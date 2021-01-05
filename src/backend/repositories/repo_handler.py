import os
from datetime import datetime

from db import dbconn
from db.db_session import session_scope
import pandas as pd


def insert(data, db_vars):
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], data.__tablename__ + ".csv")
        insert_data_to_local(data, path)
        return data
    else:
        with session_scope() as session:
            dbconn.insert(session, data)
            session.flush()
            session.refresh(data)
            session.expunge_all()
            return data


def insert_search(archive_search, db_vars):
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], archive_search.__tablename__ + ".csv")
        archive_search.timestamp = datetime.now()
        insert_data_to_local(archive_search, path)
        return archive_search.id
    else:
        with session_scope() as session:
            dbconn.insert_search(session, archive_search)
            print("Search inserted into the database", "Search id: ", archive_search.id)
            session.expunge_all()
            search_id = archive_search.id
            return search_id


def insert_data_to_local(data, path):
    _id = get_local_search_max_id(path) + 1
    df = data.to_data_frame()
    df["id"][0] = _id
    data.id = _id
    df.to_csv(path, mode='a', header=not os.path.exists(path), index=False)


def get_local_search_max_id(path):
    if os.path.exists(path):
        df = pd.read_csv(path)
        if len(df) > 0:
            return df["id"].max()
    return 0
