# vim: set fileencoding=utf-8:
import os
import utils
import model


desktop = utils.get_desktop()
save_path = os.path.join(desktop, u'账户信息.txt')

description = u"""欢迎使用BAMS %(ver)s，作者：%(author)s\n
请输入关键词：""" % {"ver": utils.__version__, "author": utils.__author__}

kw = raw_input(description.encode('gbk')).decode('gbk')
field = 'no' if kw.isdigit() else 'name'
res = model.get_acc(field, kw)

with open(save_path, 'w') as f:
  for acc in res:
    s = ' '.join(acc).strip()
    f.write(s.encode('utf8') + '\n')
