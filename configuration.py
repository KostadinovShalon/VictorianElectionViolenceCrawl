import os

import db_session


def server_variables():
    path = os.path.join("application", "configuration", "server_variables.csv")
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


def bna_variables():
    path = os.path.join("application", "configuration", "bna_user.csv")
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
            return dict(user=user, password=password)


def set_bna_variables(user, password):
    path = os.path.join("application", "configuration", "bna_user.csv")
    with open(path, "w") as f:
        f.write(f"{user};{password}")


def db_variables():
    path = os.path.join("application", "configuration", "db_connection_details.csv")
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
