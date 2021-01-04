import os

from application.db import get_db
from db import db_session


# Getters
def server_variables():
    db = get_db()
    server_cfg = db.execute("SELECT user, password, sftp_host, port FROM storage_config").fetchone()
    db_cfg = db.execute("SELECT local, path FROM db_config").fetchone()
    files_dir = None if db_cfg["path"] is None else os.path.join(db_cfg["path"], "files")
    return {
        "local": db_cfg["local"] == 1,
        "files_dir": files_dir,
        "user": server_cfg["user"],
        "password": server_cfg["password"],
        "host": server_cfg["sftp_host"]
    }


def bna_variables():
    db = get_db()
    bna_cfg = db.execute("SELECT user, password FROM bna_config").fetchone()
    return {
        "username": bna_cfg["user"],
        "password": bna_cfg["password"]
    }


def get_login_details():
    user_details = bna_variables()
    return {
        "username": user_details["username"],
        "password": user_details["password"],
        "remember_me": 'false',
        "next_page": '',

        "login_url": "https://www.britishnewspaperarchive.co.uk/account/login",

        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "www.britishnewspaperarchive.co.uk",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/64.0.3282.167 Safari/537.36",
            "Origin": "https://www.britishnewspaperarchive.co.uk",
            "Link": "<https://www.britishnewspaperarchive.co.uk/account/login>; rel=\"canonical\"",
            "X-Frame-Options": "SAMEORIGIN",
        }
    }


def db_variables():
    db = get_db()
    db_cfg = db.execute("SELECT user, password, host, port, local, path FROM db_config").fetchone()
    return {
        "user": db_cfg["user"],
        "password": db_cfg["password"],
        "host": db_cfg["host"],
        "port": db_cfg["port"],
        "local": db_cfg["local"],
        "data_dir": db_cfg["path"],
    }


# Setters


def set_server_variables(user, password, host):
    db = get_db()
    db.execute("UPDATE storage_config SET user = ?, password = ?, sftp_host = ? WHERE 1",
               (user, password, host))
    db.commit()


def set_bna_variables(user, password):
    db = get_db()
    db.execute("UPDATE bna_config SET user = ?, password = ?",
               (user, password))
    db.commit()


def set_db_variables(user, password, host, local, data_dir, port=3306):
    db = get_db()
    if local:
        db.execute("UPDATE db_config SET local = 1, path = ?",
                   (data_dir,))
    else:
        db.execute("UPDATE db_config SET local = 0, user = ?, password = ?, host = ?, port = ?",
                   (user, password, host, port))
        db_session.change_session_data(user, password, host)
    db.commit()
