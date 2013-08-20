# vim: set fileencoding=utf-8:
import os
import sys
import utils
from PyQt4 import QtGui, QtCore
from string import strip
from ui_bams import Ui_Form


class BAMS(QtGui.QWidget, Ui_Form):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
    self.setupUi(self)

    self.data = utils.get_data()
    self.clipboard = QtGui.QApplication.clipboard()

    self.initUi()
    self.show()

  def initUi(self):
    title = u"BAMS %(version)s - 作者：%(author)s" % \
        {"version": utils.__version__, "author": utils.__author__}
    self.setWindowTitle(title)
    self.setWindowIcon(QtGui.QIcon(os.path.join("resources", "bams.png")))
    self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
    self.setFixedSize(740, 465)

    self.leSearch.setFocus()
    self.lwResult.setSortingEnabled(1)
    self.initTwResult()

    self.leSearch.returnPressed.connect(self.display)
    self.lwResult.itemClicked.connect(self.setTwResult)
    self.twResult.itemClicked.connect(self.copy)

  def initTwResult(self):
    tableWidth = self.twResult.size().width()
    count = len(self.data[0])
    colWidth = int(tableWidth/count)

    self.twResult.setRowCount(1)
    self.twResult.setColumnCount(count)
    #self.twResult.setShowGrid(False)
    #self.twResult.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
    self.twResult.horizontalHeader().setVisible(False)
    self.twResult.verticalHeader().setVisible(False)
    self.twResult.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    for i in range(count):
      self.twResult.setColumnWidth(i, colWidth)

  def setTwResult(self, item):
    info = unicode(item.text()).split()
    item = lambda s: QtGui.QTableWidgetItem(s)

    for i in range(self.twResult.columnCount()):
      self.twResult.setItem(0, i, item(info[i]))

  @QtCore.pyqtSignature("")
  def on_pbSearch_clicked(self):
    self.display()

  def search(self):
    kw = unicode(self.leSearch.text())
    if len(kw) == 0:
      return []
    col = 0 if kw.isdigit() else 1 # 按账号或账户搜索

    res = [acc for acc in self.data if kw in acc[col]]
    return res

  def display(self):
    self.lwResult.clear()
    self.twResult.clearContents()

    kws = self.search()
    for i in range(len(kws)):
      s = ' '.join(map(strip, kws[i]))
      self.lwResult.insertItem(i, QtGui.QListWidgetItem(s))

  def copy(self, item):
    info = item.text()
    self.clipboard.setText(info)
    QtGui.QToolTip.showText(QtGui.QCursor.pos(), u"内容已复制")


def main():
  utils.setappid()
  app = QtGui.QApplication(sys.argv)
  widget = BAMS()
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()
