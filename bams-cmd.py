# vim: set fileencoding=utf-8:
import os
import utils


desktop = utils.get_desktop()
save_path = os.path.join(desktop, u'账户信息.txt')
acc_list = utils.get_data()

description = u"""欢迎使用BAMS %(ver)s，作者：%(author)s\n
请输入关键词：""" % {"ver": utils.__version__, "author": utils.__author__}

kw = raw_input(description.encode('gbk')).decode('gbk')
col = 0 if kw.isdigit() else 1
res = [acc for acc in acc_list if kw in acc[col]]

with open(save_path, 'w') as f:
  for acc in res:
    s = "%s %s %s %s %s" % acc
    f.write(s.encode('utf8') + '\r\n')
