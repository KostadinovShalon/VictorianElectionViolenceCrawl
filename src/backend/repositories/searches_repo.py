import os
from datetime import datetime

import pandas as pd
from sqlalchemy import func

from repositories import configuration
from db.databasemodels import ArchiveSearch, ArchiveSearchCount
from db.db_session import session_scope

time_format = "%Y-%m-%d"


def get_searches(limit, page, sort_by, sort_desc):
    results = None
    total = 0
    db_vars = configuration.db_variables()
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{ArchiveSearch.__tablename__}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            total = len(df)
            if sort_by is not None and sort_by in ["id", "start_date", "end_date", "keyword", "timestamp"]:
                if sort_by == "id":
                    df.sort_values(by=['id'], ascending=not sort_desc, inplace=True, ignore_index=True)
                elif sort_by == "start_date":
                    df.sort_values(by=['archive_date_start'], ascending=not sort_desc, inplace=True, ignore_index=True)
                elif sort_by == "end_date":
                    df.sort_values(by=['archive_date_end'], ascending=not sort_desc, inplace=True, ignore_index=True)
                elif sort_by == "keyword":
                    df.sort_values(by=['search_text'], ascending=not sort_desc, inplace=True, ignore_index=True)
                else:
                    df.sort_values(by=['timestamp'], ascending=not sort_desc, inplace=True, ignore_index=True)
            else:
                df.sort_values(by=['id'], ascending=False, inplace=True, ignore_index=True)

            df = df.iloc[limit*page:limit*page + limit]
            total = len(df)
            results = []
            for _, d in df.iterrows():
                d = d.where(pd.notnull(d), None)
                adde = datetime.strptime(d.added_date_end, time_format) \
                    if isinstance(d.added_date_end, str) else None
                adds = datetime.strptime(d.added_date_start, time_format) \
                    if isinstance(d.added_date_start, str) else None
                tmstmp = datetime.strptime(d.timestamp, "%Y-%m-%d %H:%M:%S") \
                    if isinstance(d.timestamp, str) else None
                load = {
                    'id': d["id"],
                    'archive': d["archive"],
                    'search_text': d["search_text"],
                    'archive_date_start': d["archive_date_start"],
                    'archive_date_end': d["archive_date_end"],
                    'search_batch_id': d["search_batch_id"],
                    'added_date_end': adde,
                    'added_date_start': adds,
                    'article_type': d["article_type"],
                    'exact_phrase': d["exact_phrase"],
                    'exact_search': d["exact_search"],
                    'exclude_words': d["exclude_words"],
                    'front_page': d["front_page"],
                    'newspaper_title': d["newspaper_title"],
                    'publication_place': d["publication_place"],
                    'search_all_words': d["search_all_words"],
                    'sort_by': d["sort_by"],
                    'tags': d["tags"],
                    'timestamp': tmstmp,
                }
                results.append(ArchiveSearch(**load))
    else:
        with session_scope() as session:
            results = session.query(ArchiveSearch)
            if sort_by is not None and sort_by in ["id", "start_date", "end_date", "keyword", "timestamp"]:
                if sort_by == "id":
                    results = results.order_by(ArchiveSearch.id.desc()) if sort_desc else results.order_by(
                        ArchiveSearch.id)
                elif sort_by == "start_date":
                    results = results.order_by(ArchiveSearch.archive_date_start.desc()) if sort_desc \
                        else results.order_by(ArchiveSearch.archive_date_start)
                elif sort_by == "end_date":
                    results = results.order_by(ArchiveSearch.archive_date_end.desc()) if sort_desc \
                        else results.order_by(ArchiveSearch.archive_date_end)
                elif sort_by == "keyword":
                    print("In keyword. Desc: ", sort_desc, sort_desc if sort_desc else None)
                    results = results.order_by(ArchiveSearch.search_text.desc()) if sort_desc \
                        else results.order_by(ArchiveSearch.search_text)
                else:
                    results = results.order_by(ArchiveSearch.timestamp.desc()) if sort_desc \
                        else results.order_by(ArchiveSearch.timestamp)
            else:
                results = results.order_by(ArchiveSearch.id.desc())
            results = results.limit(limit).offset(limit * page).all()
            total = session.query(func.count(ArchiveSearch.id)).first()[0]
            session.expunge_all()
    if results is not None:
        results = [r.to_dict() for r in results]
    return results, total


def get_searches_count(limit, page, sort_by, sort_desc):
    results = None
    total = 0
    db_vars = configuration.db_variables()
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{ArchiveSearchCount.__tablename__}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            total = len(df)
            if sort_by is not None and sort_by in ["id", "start_date", "end_date", "keyword", "timestamp", "count"]:
                if sort_by == "id":
                    df.sort_values(by=['id'], ascending=not sort_desc, inplace=True, ignore_index=True)
                elif sort_by == "start_date":
                    df.sort_values(by=['archive_date_start'], ascending=not sort_desc, inplace=True, ignore_index=True)
                elif sort_by == "end_date":
                    df.sort_values(by=['archive_date_end'], ascending=not sort_desc, inplace=True, ignore_index=True)
                elif sort_by == "keyword":
                    df.sort_values(by=['search_text'], ascending=not sort_desc, inplace=True, ignore_index=True)
                elif sort_by == "count":
                    df.sort_values(by=['results_count'], ascending=not sort_desc, inplace=True, ignore_index=True)
                else:
                    df.sort_values(by=['timestamp'], ascending=not sort_desc, inplace=True, ignore_index=True)
            else:
                df.sort_values(by=['id'], ascending=False, inplace=True, ignore_index=True)

            df = df.iloc[limit*page:limit*page + limit]

            results = []
            for _, d in df.iterrows():
                d = d.where(pd.notnull(d), None)
                adde = datetime.strptime(d.added_date_end, time_format) \
                    if isinstance(d.added_date_end, str) else None
                adds = datetime.strptime(d.added_date_start, time_format) \
                    if isinstance(d.added_date_start, str) else None
                tmstmp = datetime.strptime(d.timestamp, "%Y-%m-%d %H:%M:%S") \
                    if isinstance(d.timestamp, str) else None
                load = {
                    'id': d["id"],
                    'search_text': d["search_text"],
                    'archive_date_start': d["archive_date_start"],
                    'archive_date_end': d["archive_date_end"],
                    'search_batch_id': d["search_batch_id"],
                    'added_date_end': adde,
                    'added_date_start': adds,
                    'article_type': d["article_type"],
                    'exact_phrase': d["exact_phrase"],
                    'exact_search': d["exact_search"],
                    'exclude_words': d["exclude_words"],
                    'front_page': d["front_page"],
                    'newspaper_title': d["newspaper_title"],
                    'publication_place': d["publication_place"],
                    'search_all_words': d["search_all_words"],
                    'sort_by': d["sort_by"],
                    'tags': d["tags"],
                    'timestamp': tmstmp,
                    'results_count': d['results_count']
                }
                results.append(ArchiveSearchCount(**load))
    else:
        with session_scope() as session:
            results = session.query(ArchiveSearchCount)
            if sort_by is not None and sort_by in ["id", "start_date", "end_date", "keyword", "timestamp", "count"]:
                if sort_by == "id":
                    results = results.order_by(ArchiveSearchCount.id.desc()) if sort_desc \
                        else results.order_by(ArchiveSearchCount.id)
                elif sort_by == "start_date":
                    results = results.order_by(ArchiveSearchCount.archive_date_start.desc()) if sort_desc \
                        else results.order_by(ArchiveSearchCount.archive_date_start)
                elif sort_by == "end_date":
                    results = results.order_by(ArchiveSearchCount.archive_date_end.desc()) if sort_desc \
                        else results.order_by(ArchiveSearchCount.archive_date_end)
                elif sort_by == "keyword":
                    results = results.order_by(ArchiveSearchCount.search_text.desc()) if sort_desc \
                        else results.order_by(ArchiveSearchCount.search_text)
                elif sort_by == "count":
                    results = results.order_by(ArchiveSearchCount.results_count.desc()) if sort_desc \
                        else results.order_by(ArchiveSearchCount.results_count)
                else:
                    results = results.order_by(ArchiveSearchCount.timestamp.desc()) if sort_desc \
                        else results.order_by(ArchiveSearchCount.timestamp)
            else:
                results = results.order_by(ArchiveSearchCount.id.desc())
            results = results.limit(limit).offset(limit * page).all()
            total = session.query(func.count(ArchiveSearchCount.id)).first()[0]
            session.expunge_all()
    if results is not None:
        results = [r.to_dict() for r in results]
    return results, total


def get_total_searches():
    total = 0

    db_vars = configuration.db_variables()
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{ArchiveSearch.__tablename__}.csv")
        if os.path.exists(path):
            total = len(pd.read_csv(path))
    else:
        with session_scope() as session:
            total = session.query(func.count(ArchiveSearch.id)).first()[0]
            session.expunge_all()
    return total
