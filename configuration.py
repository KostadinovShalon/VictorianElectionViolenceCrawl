import os
import yaml

from db import db_session


basic_config = {
        "local": {
            "enabled": False,
            "data_dir": None,
            "files_dir": "files",
        },
        "bna": {
            "user": None,
            "password": None
        },
        "db": {
            "user": None,
            "password": None,
            "host": None,
            "port": 3306
        },
        "files": {
            "user": None,
            "password": None,
            "sftp_host": None
        }
    }


# Getters
def server_variables(prepend='.'):
    path = os.path.join(prepend, "application", "configuration", "cfg.yaml")
    if not os.path.exists(path):
        write_config(path, basic_config)
    with open(path, "r") as f:
        cfg = yaml.full_load(f)
    files_dir = None if cfg["local"]["data_dir"] is None or cfg["local"]["files_dir"] is None else \
        os.path.join(cfg["local"]["data_dir"], cfg["local"]["files_dir"])
    return {
        "local": cfg["local"]["enabled"],
        "files_dir": files_dir,
        "user": cfg["files"]["user"],
        "password": cfg["files"]["password"],
        "host": cfg["files"]["sftp_host"]
    }


def bna_variables(prepend="."):
    path = os.path.join(prepend, "application", "configuration", "cfg.yaml")
    if not os.path.exists(path):
        write_config(path, basic_config)
    with open(path, "r") as f:
        cfg = yaml.full_load(f)
    return {
        "username": cfg["bna"]["user"],
        "password": cfg["bna"]["password"]
    }


def get_login_details(prepend="."):
    user_details = bna_variables(prepend)
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


def db_variables(prepend='.'):
    path = os.path.join(prepend, "application", "configuration", "cfg.yaml")
    if not os.path.exists(path):
        write_config(path, basic_config)
    with open(path, "r") as f:
        cfg = yaml.full_load(f)
    return {
        "user": cfg["db"]["user"],
        "password": cfg["db"]["password"],
        "host": cfg["db"]["host"],
        "port": cfg["db"]["port"],
        "local": cfg["local"]["enabled"],
        "data_dir": cfg["local"]["data_dir"],
    }


# Setters
def _get_cfg(path):
    if not os.path.exists(path):
        return dict(basic_config)
    else:
        return yaml.full_load(open(path, "r"))


def set_server_variables(user, password, host, prepend='.'):
    path = os.path.join(prepend, "application", "configuration", "cfg.yaml")
    cfg = _get_cfg(path)
    cfg["files"]["user"] = user
    cfg["files"]["password"] = password
    cfg["files"]["sftp_host"] = host
    write_config(path, cfg)


def set_bna_variables(user, password, prepend='.'):
    path = os.path.join(prepend, "application", "configuration", "cfg.yaml")
    cfg = _get_cfg(path)
    cfg["bna"]["user"] = user
    cfg["bna"]["password"] = password
    write_config(path, cfg)


def set_db_variables(user, password, host, local, data_dir, files_dir="files", port=3306, prepend='.'):
    if local:
        path = os.path.join(prepend, "application", "configuration", "cfg.yaml")
        cfg = _get_cfg(path)
        cfg["local"]["enabled"] = local
        if local:
            cfg["local"]["data_dir"] = data_dir
            cfg["local"]["files_dir"] = files_dir
        write_config(path, cfg)
    else:
        path = os.path.join(prepend, "application", "configuration", "cfg.yaml")
        cfg = _get_cfg(path)
        cfg["db"]["user"] = user
        cfg["db"]["password"] = password
        cfg["db"]["host"] = host
        cfg["db"]["port"] = port
        cfg["local"]["enabled"] = False
        write_config(path, cfg)
        db_session.change_session_data(user, password, host)



def write_config(path, cfg):
    with open(path, 'w') as file:
        yaml.dump(cfg, file)
