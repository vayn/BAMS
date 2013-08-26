CREATE TABLE account (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  acc_no TEXT,
  acc_name TEXT,
  counter TEXT,
  area TEXT);

CREATE UNIQUE INDEX data_idx ON account(acc_no, counter);

CREATE VIRTUAL TABLE v_account USING fts4(
  idx_name TEXT,
  source_id INTEGER);

CREATE TRIGGER v_account_update
  AFTER UPDATE ON account BEGIN
    UPDATE v_account SET idx_name = NEW.acc_name
    WHERE source_id=NEW.id;
END;

CREATE TRIGGER v_account_delete
  AFTER DELETE ON account BEGIN
    DELETE FROM v_account WHERE source_id=OLD.id;
END;
