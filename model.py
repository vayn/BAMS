# vim: set fileencoding=utf-8:
import os
import sys
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
            text = 'None'
        elif text is None:
          text = 'None'
        info.append(text)
      acc.append(info)

    return acc

  def cmb_handler(self, raw_data):
    doc = open(raw_data, 'r').readlines()
    acc = []

    for l in doc:
      acc.append(map(lambda e: unicode(e, 'gbk'), l.split(',')))

    return acc


def get_acc(field, kw):
  kw = ' '.join(kw.replace(' ', ''))
  stmt = """SELECT acc_no, acc_name, counter, area
  FROM account AS acc JOIN (
  SELECT source_id FROM v_account WHERE idx_%(field)s MATCH ? LIMIT 50) AS vacc
  WHERE acc.id=vacc.source_id;""" % {'field': field}
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
  v_stmt = """INSERT OR REPLACE INTO v_account (idx_no, idx_name, source_id)
  VALUES (?, ?, ?);"""

  for acc in data:
    field = {
      "id": None,
      "acc_no": ' '.join(acc[0]),
      "acc_name": ' '.join(acc[1]),
      "counter": acc[2],
      "area": acc[3]
    }
    sid = cur.execute(r_stmt, field).lastrowid
    cur.execute(v_stmt, (field['acc_no'], field['acc_name'], sid))

  conn.commit()


if __name__ == "__main__":
  if sys.argv[1] == 'bootstrap':
    create_db()
  elif len(sys.argv) == 3:
    bank, raw_data = sys.argv[1:]
    insert_db(bank, raw_data)
