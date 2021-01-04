DROP TABLE IF EXISTS bna_config;
DROP TABLE IF EXISTS db_config;
DROP TABLE IF EXISTS storage_config;
DROP TABLE IF EXISTS local_config;

CREATE TABLE bna_config (
  user TEXT UNIQUE NULL,
  password TEXT NULL
);

CREATE TABLE db_config (
  user TEXT NULL,
  password TEXT NULL,
  host TEXT NULL,
  port INTEGER NULL DEFAULT 3306,
  local INTEGER NOT NULL DEFAULT 0,
  path TEXT NULL
);

CREATE TABLE storage_config (
  user TEXT UNIQUE NULL,
  password TEXT NULL,
  sftp_host TEXT NULL,
  port INTEGER NULL DEFAULT 22
);

INSERT INTO bna_config VALUES (null, null);
INSERT INTO db_config VALUES (null, null, null, 3306, 0, null);
INSERT INTO storage_config VALUES (null, null, null, 22);