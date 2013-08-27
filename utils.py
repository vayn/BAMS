# vim: set fileencoding=utf-8:
import os
import ctypes
import _winreg as winreg


__author__ = "Vayn a.k.a. VT <vayn@vayn.de>"
__version__ = '0.7.1'


def setappid():
  u"""设置 AppID
  
  可以避免因与 Python 的 AppID 相同而在任务栏被折叠
  注意：仅在 Windows XP 以上版本有效
  
  """
  try:
    myappid = "VT.BAMS.%s" % __version__
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
  except AttributeError:
    pass

def get_desktop():
  key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,\
      r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
  return winreg.QueryValueEx(key, 'Desktop')[0]
