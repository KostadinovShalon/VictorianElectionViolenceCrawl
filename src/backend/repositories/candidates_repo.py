import os
from datetime import datetime

from db.databasemodels import CandidateDocument, ArchiveSearchResult
from db.db_session import session_scope
import pandas as pd

time_format = "%Y-%m-%d"


def get_candidate_id_from_url(url, db_vars):
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{CandidateDocument.__tablename__}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            candidate_with_url = df[df["url"] == url]
            if len(candidate_with_url) > 0:
                return candidate_with_url.iloc[0].id
    else:
        with session_scope() as session:
            result = session.query(CandidateDocument.id) \
                .filter(CandidateDocument.url == url).first()
            session.expunge_all()
            if result is not None:
                return result.id
    return None


def get_candidate_url_from_id(candidate_id, db_vars):
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{CandidateDocument.__tablename__}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            candidate_with_url = df[df["id"] == candidate_id]
            if len(candidate_with_url) > 0:
                return candidate_with_url.iloc[0].url
    else:
        with session_scope() as session:
            result = session.query(CandidateDocument.url) \
                .filter(CandidateDocument.id == candidate_id).first()
            session.expunge_all()
            if result is not None:
                return result.url
    return None


def update_candidate_status(candidate_id, status, g_status, status_writer, db_vars):
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{CandidateDocument.__tablename__}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            df.loc[df.id == candidate_id, ("status", "g_status", "status_writer")] = \
                str(status), str(g_status), status_writer
            df.to_csv(path, mode='w', index=False)
    else:
        with session_scope() as session:
            session.query(CandidateDocument). \
                filter(CandidateDocument.id == candidate_id). \
                update(values={"status": status, "g_status": g_status, "status_writer": status_writer})
            session.commit()


def update_candidate_ocr(candidate_id, ocr, db_vars):
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{CandidateDocument.__tablename__}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            df.loc[df.id == candidate_id, "ocr"] = ocr
            df.to_csv(path, mode='w', index=False)
    else:
        with session_scope() as session:
            session.query(CandidateDocument). \
                filter(CandidateDocument.id == candidate_id). \
                update(values={"ocr": ocr})
            session.commit()


def get_candidate(candidate_id, db_vars):
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{CandidateDocument.__tablename__}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            candidate = df.loc[df.id == candidate_id].iloc[0]
            candidate = candidate.where(pd.notnull(candidate), None)
            pub_date = datetime.strptime(candidate.publication_date, time_format) \
                if isinstance(candidate.publication_date, str) else None
            return CandidateDocument(
                id=candidate.id,
                title=candidate.title,
                url=candidate.url,
                description=candidate.description,
                publication_title=candidate.publication_title,
                publication_location=candidate.publication_location,
                type=candidate.type,
                status=candidate.status,
                page=candidate.page,
                publication_date=pub_date,
                word_count=candidate.word_count,
                ocr=candidate.ocr,
                g_status=candidate.g_status,
                status_writer=candidate.status_writer)

        else:
            return None
    else:
        with session_scope() as session:
            candidate = session.query(CandidateDocument).filter(CandidateDocument.id == candidate_id).first()
            session.expunge_all()
            return candidate


def get_candidates(ids, limit, page, sort_by, sort_desc, db_vars):
    cands, total = [], 0
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{CandidateDocument.__tablename__}.csv")
        search_result_path = os.path.join(db_vars["data_dir"], f"{ArchiveSearchResult.__tablename__}.csv")
        if os.path.exists(path):
            needing_coding = pd.read_csv(path)
            needing_coding = needing_coding.loc[needing_coding.status != 0].loc[needing_coding.status != 1]
            if ids is not None and os.path.exists(search_result_path):
                results_df = pd.read_csv(search_result_path)
                results_df = results_df.loc[results_df.archive_search_id.isin(ids)]
                needing_coding = needing_coding.loc[needing_coding.url.isin(results_df.url.values)]
            total = len(needing_coding)
            if sort_by is not None and sort_by in ["id", "title", "publication_title", "publication_location", "status",
                                                   "publication_date", "description"]:
                if sort_by == "id":
                    needing_coding.sort_values(by=['id'], ascending=not sort_desc, inplace=True, ignore_index=True)
                elif sort_by == "description":
                    needing_coding.sort_values(by=['description'], ascending=not sort_desc,
                                               inplace=True, ignore_index=True)
                elif sort_by == "title":
                    needing_coding.sort_values(by=['title'], ascending=not sort_desc,
                                               inplace=True, ignore_index=True)
                elif sort_by == "publication_title":
                    needing_coding.sort_values(by=['publication_title'], ascending=not sort_desc,
                                               inplace=True, ignore_index=True)
                elif sort_by == "publication_location":
                    needing_coding.sort_values(by=['publication_location'], ascending=not sort_desc,
                                               inplace=True, ignore_index=True)
                elif sort_by == "status":
                    needing_coding.sort_values(by=['status'], ascending=not sort_desc, inplace=True, ignore_index=True)
                else:
                    needing_coding.sort_values(by=['publication_date'], ascending=not sort_desc,
                                               inplace=True, ignore_index=True)
            else:
                needing_coding.sort_values(by=['id'], ascending=False, inplace=True, ignore_index=True)

            needing_coding = needing_coding.iloc[limit * page:limit * page + limit]

            for _, d in needing_coding.iterrows():
                d = d.where(pd.notnull(d), None)
                pub_date = datetime.strptime(d.publication_date, time_format) \
                    if isinstance(d.publication_date, str) else None

                load = {
                    'id': d.id,
                    'title': d.title,
                    'url': d.url,
                    'description': d.description,
                    'publication_title': d.publication_title,
                    'publication_location': d.publication_location,
                    'type': d.type,
                    'status': d.status,
                    'page': d.page,
                    'publication_date': pub_date,
                    'word_count': d.word_count,
                    'ocr': d.ocr,
                    'g_status': d.g_status,
                    'status_writer': d.status_writer
                }
                cands.append(CandidateDocument(**load))
    else:
        with session_scope() as session:
            needing_coding = session.query(CandidateDocument) \
                .filter(CandidateDocument.status.notin_(('0', '1')))
            if ids is not None:
                results = session.query(ArchiveSearchResult.url) \
                    .filter(ArchiveSearchResult.archive_search_id.in_(ids))
                needing_coding = needing_coding.filter(CandidateDocument.url.in_(results))
            if sort_by is not None and sort_by in ["id", "title", "publication_title", "publication_location", "status",
                                                   "publication_date", "description"]:
                if sort_by == "id":
                    needing_coding = needing_coding.order_by(CandidateDocument.id.desc()) if sort_desc \
                        else needing_coding.order_by(CandidateDocument.id)
                if sort_by == "description":
                    needing_coding = needing_coding.order_by(CandidateDocument.description.desc()) if sort_desc \
                        else needing_coding.order_by(CandidateDocument.description)
                elif sort_by == "title":
                    needing_coding = needing_coding.order_by(CandidateDocument.title.desc()) if sort_desc \
                        else needing_coding.order_by(CandidateDocument.title)
                elif sort_by == "publication_title":
                    needing_coding = needing_coding.order_by(CandidateDocument.publication_title.desc()) if sort_desc \
                        else needing_coding.order_by(CandidateDocument.publication_title)
                elif sort_by == "publication_location":
                    needing_coding = needing_coding.order_by(CandidateDocument.publication_location.desc()) \
                        if sort_desc else needing_coding.order_by(CandidateDocument.publication_location)
                elif sort_by == "status":
                    needing_coding = needing_coding.order_by(CandidateDocument.status.desc()) if sort_desc \
                        else needing_coding.order_by(CandidateDocument.status)
                else:
                    needing_coding = needing_coding.order_by(CandidateDocument.publication_date.desc()) if sort_desc \
                        else needing_coding.order_by(CandidateDocument.publication_date)
            else:
                needing_coding = needing_coding.order_by(CandidateDocument.id.desc())
            cands = needing_coding.limit(limit).offset(limit * page).all()
            total = get_remote_count_candidates(ids)
            session.expunge_all()
    if cands is not None:
        cands = [r.to_dict() for r in cands]
    return cands, total


def get_remote_count_candidates(ids=None):
    with session_scope() as session:
        results = session.query(CandidateDocument.id) \
            .filter(CandidateDocument.status.notin_(("0", "1")))
        if ids is not None:
            search_urls = session.query(ArchiveSearchResult.url) \
                .filter(ArchiveSearchResult.archive_search_id.in_(ids))
            results = results.filter(CandidateDocument.url.in_(search_urls))
        session.expunge_all()
    return results.count()


def get_total_candidates(db_vars):
    total = 0
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{CandidateDocument.__tablename__}.csv")
        if os.path.exists(path):
            cands = pd.read_csv(path)
            cands = cands.loc[cands.status != 0].loc[cands.status != 1]
            total = len(cands)
    else:
        total = get_remote_count_candidates()
    return total
