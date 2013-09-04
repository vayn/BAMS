# vim: set fileencoding=utf-8:
import os
import sys
import struct
from lxml import etree
from pysqlite2 import dbapi2 as sqlite3


db = os.path.join('resources', 'acc.dat')
conn = sqlite3.connect(db)
cur = conn.cursor()


class ImportData:
  def __init__(self, bank, raw_data):
    self.data = None
    method = getattr(self, bank+'_handler', None)
    if callable(method):
      self.data = method(raw_data)

  def __call__(self):
    return self.data

  def ccb_handler(self, raw_data):
    idx_list = ['RcvAccNo', 'RcvAccName', 'CounterName', 'BranchName']

    doc = etree.parse(raw_data).getroot()
    acc = []

    for el in doc:
      info = []
      for idx in idx_list:
        text = el.find(idx).text
        if (idx == 'BranchName') and (text is None):
          text = el.find('AreaProv').text
          if text is None:
            text = ''
        elif text is None:
          text = ''
        info.append(text)
      acc.append(info)

    return acc

  def cmb_handler(self, raw_data):
    doc = open(raw_data, 'r').readlines()
    acc = []

    for l in doc:
      acc.append(map(lambda e: unicode(e, 'gbk'), l.split(',')))

    return acc

  def beijing_handler(self, raw_data):
    idx_list = ['AccNo', 'Name', 'RecOpenAccBranchName', 'ReceeArea']

    doc = etree.parse(raw_data).getroot().find('ReceeList')
    acc = []

    for el in doc:
      attrib = el.attrib
      acc.append([attrib[idx] for idx in idx_list])

    return acc


def make_rank_func(weights):
  def rank(matchinfo):
    matchinfo = struct.unpack("I"*(len(matchinfo)/4), matchinfo)
    it = iter(matchinfo[2:])
    return sum(x[0]*w/x[1]
        for x, w in zip(zip(it, it, it), weights) if x[1])
  return rank

def get_acc(field, kw):
  conn.create_function("rank", 1, make_rank_func((1., .1, 0, 0)))

  if field == 'name':
    kw = ' '.join(kw.replace(' ', ''))
    stmt = """SELECT acc_no, acc_name, counter, area
    FROM account AS acc JOIN (
      SELECT rank(matchinfo(v_account)) AS r, source_id FROM v_account
      WHERE idx_name MATCH ?) AS vacc
    WHERE acc.id=vacc.source_id ORDER BY vacc.r DESC LIMIT 50;"""
  elif field == 'no':
    stmt = """SELECT acc_no, acc_name, counter, area
    FROM account WHERE instr(acc_no, ?)"""
  cur.execute(stmt, (kw,))
  res = cur.fetchall()
  acc = []
  for info in res:
    acc.append(map(lambda x: x.replace(' ', ''), info))
  return acc

def create_db():
  sql = open("sqlite3.sql").read()
  cur.executescript(sql)

def insert_db(bank, raw_data):
  data = ImportData(bank, os.path.join('resources', raw_data))()

  r_stmt = """INSERT OR REPLACE INTO account (id, acc_no, acc_name, counter,
  area) VALUES (:id, :acc_no, :acc_name, :counter, :area);"""
  v_stmt = """INSERT OR REPLACE INTO v_account (idx_name, source_id)
  VALUES (?, ?);"""

  for acc in data:
    acc = map(lambda x: x.strip(), acc) # 删除多余空格
    field = {
      "id": None,
      "acc_no": acc[0],
      "acc_name": ' '.join(acc[1]),
      "counter": acc[2],
      "area": acc[3]
    }
    sid = cur.execute(r_stmt, field).lastrowid
    cur.execute(v_stmt, (field['acc_name'], sid))

  conn.commit()


if __name__ == "__main__":
  if sys.argv[1] == 'bootstrap':
    create_db()
  elif len(sys.argv) == 3:
    bank, raw_data = sys.argv[1:]
    insert_db(bank, raw_data)
