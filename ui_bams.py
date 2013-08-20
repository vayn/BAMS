# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_bams.ui'
#
# Created: Tue Aug 20 03:19:44 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(740, 465)
        self.gbSearch = QtGui.QGroupBox(Form)
        self.gbSearch.setGeometry(QtCore.QRect(20, 20, 701, 91))
        self.gbSearch.setStyleSheet(_fromUtf8(""))
        self.gbSearch.setObjectName(_fromUtf8("gbSearch"))
        self.leSearch = QtGui.QLineEdit(self.gbSearch)
        self.leSearch.setGeometry(QtCore.QRect(20, 30, 541, 31))
        self.leSearch.setToolTip(_fromUtf8(""))
        self.leSearch.setStyleSheet(_fromUtf8("background-image: url(\"resources/search_bg.png\");\n"
"background-repeat: no-repeat;\n"
"background-position: center right;\n"
"padding-right: 17px;"))
        self.leSearch.setText(_fromUtf8(""))
        self.leSearch.setObjectName(_fromUtf8("leSearch"))
        self.pbSearch = QtGui.QPushButton(self.gbSearch)
        self.pbSearch.setGeometry(QtCore.QRect(570, 30, 111, 31))
        self.pbSearch.setObjectName(_fromUtf8("pbSearch"))
        self.gbResult = QtGui.QGroupBox(Form)
        self.gbResult.setGeometry(QtCore.QRect(20, 120, 701, 331))
        self.gbResult.setObjectName(_fromUtf8("gbResult"))
        self.lwResult = QtGui.QListWidget(self.gbResult)
        self.lwResult.setGeometry(QtCore.QRect(20, 60, 661, 251))
        self.lwResult.setStyleSheet(_fromUtf8("font: 10pt \"新宋体\";"))
        self.lwResult.setObjectName(_fromUtf8("lwResult"))
        self.twResult = QtGui.QTableWidget(self.gbResult)
        self.twResult.setGeometry(QtCore.QRect(20, 20, 661, 31))
        self.twResult.setObjectName(_fromUtf8("twResult"))
        self.twResult.setColumnCount(0)
        self.twResult.setRowCount(0)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "BAMS", None))
        self.gbSearch.setTitle(_translate("Form", "搜索账户信息", None))
        self.leSearch.setPlaceholderText(_translate("Form", "请输入关键词，如「北京」", None))
        self.pbSearch.setText(_translate("Form", "搜索", None))
        self.gbResult.setTitle(_translate("Form", "搜索结果", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

