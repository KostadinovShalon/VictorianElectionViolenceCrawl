import os

from db import db_session


def server_variables(prepend='.'):
    path = os.path.join(prepend, "application", "configuration", "server_variables.csv")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("")
        return None
    with open(path, "r") as f:
        for line in f:
            variables = line.split(";")
            if len(variables) < 3:
                return None
            result = {
                "user": variables[0],
                "password": variables[1],
                "host": variables[2]
            }
            return result


def set_server_variables(user, password, host):
    path = os.path.join("application", "configuration", "server_variables.csv")
    with open(path, "w") as f:
        f.write(f"{user};{password};{host}")


def bna_variables(prepend="./"):
    path = os.path.join(prepend, "application", "configuration", "bna_user.csv")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("")
        return None
    with open(path, "r") as f:
        for line in f:
            variables = line.split(";")
            if len(variables) < 2:
                return None
            user = variables[0]
            password = variables[1]
            return dict(username=user, password=password)


def get_login_details(prepend="./"):
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


def set_bna_variables(user, password):
    path = os.path.join("application", "configuration", "bna_user.csv")
    with open(path, "w") as f:
        f.write(f"{user};{password}")


def db_variables(prepend='./'):
    path = os.path.join(prepend, "application", "configuration", "db_connection_details.csv")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("")
        return None
    with open(path, "r") as f:
        for line in f:
            variables = line.split(";")
            if len(variables) < 4:
                return None
            user = variables[0]
            password = variables[1]
            host = variables[2]
            port = variables[3]
            return dict(user=user, password=password, host=host)


def set_db_variables(user, password, host, port=3600):
    path = os.path.join("application", "configuration", "db_connection_details.csv")
    with open(path, "w") as f:
        f.write(f"{user};{password};{host};{port}")
        db_session.change_session_data(user, password, host)
