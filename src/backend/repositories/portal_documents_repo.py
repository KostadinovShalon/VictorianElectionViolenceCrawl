import os
from datetime import datetime

from sqlalchemy import func

from db.databasemodels import PortalDocument
from db.db_session import session_scope
import pandas as pd

from db.dbconn import update_page_url, update_art_url

time_format = "%Y-%m-%d"


def check_if_portal_exists(ocr, download_page, db_vars):
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{PortalDocument.__tablename__}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            cie = df.loc[df.ocr == ocr].loc[df.url == download_page]
            _id = cie.iloc[0].id if len(cie) > 0 else 0
            return len(cie) > 0, _id
        else:
            return False, 0
    else:
        with session_scope() as session:
            check_if_exists = session.query(PortalDocument) \
                .filter(PortalDocument.ocr == ocr) \
                .filter(PortalDocument.url == download_page).all()
            session.expunge_all()
            cie = len(check_if_exists) > 0
            _id = check_if_exists[0].id if cie else 0
        return cie, _id


def update_portal_page_url(document_id, db_vars, local_path=None):
    if db_vars["local"] and local_path is not None:
        path = os.path.join(db_vars["data_dir"], f"{PortalDocument.__tablename__}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            df.loc[df.id == document_id, "pdf_page_location"] = local_path
            df.to_csv(path, mode='w', index=False)
    else:
        page_url = f"/static/documents/{document_id}/page.pdf"
        with session_scope() as session:
            update_page_url(session, document_id, page_url)


def update_portal_cropped_url(document_id, db_vars, local_path=None):
    if db_vars["local"] and local_path is not None:
        path = os.path.join(db_vars["data_dir"], f"{PortalDocument.__tablename__}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            df.loc[df.id == document_id, "pdf_location"] = local_path
            df.to_csv(path, mode='w', index=False)
    else:
        page_url = f"/static/documents/{document_id}/art.pdf"
        with session_scope() as session:
            update_art_url(session, document_id, page_url)


def get_portal_document(document_id, db_vars):
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{PortalDocument.__tablename__}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            document = df.loc[df.id == document_id].iloc[0]
            document = document.where(pd.notnull(document), None)
            pub_date = datetime.strptime(document.publication_date, time_format) \
                if isinstance(document.publication_date, str) else None
            return PortalDocument(
                id=document.id,
                source_id=document.source_id,
                doc_title=document.doc_title,
                pdf_location=document.pdf_location,
                pdf_page_location=document.pdf_page_location,
                ocr=document.ocr,
                pdf_thumbnail_location=document.pdf_thumbnail_location,
                candidate_document_id=document.candidate_document_id,
                description=document.description,
                publication_date=pub_date,
                publication_location=document.publication_location,
                publication_title=document.publication_title,
                type=document.type,
                url=document.url,
                word_count=document.word_count)
        else:
            return None
    else:
        with session_scope() as session:
            document = session.query(PortalDocument).filter(PortalDocument.id == document_id).first()
            session.expunge_all()
            return document


def get_portal_documents(limit, page, sort_by, sort_desc, db_vars):
    docs, total = [], 0
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{PortalDocument.__tablename__}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)

            if sort_by is not None and sort_by in ["id", "title", "publication_title", "publication_location",
                                                   "publication_date", "type", "word_count", "description"]:
                if sort_by == "id":
                    df.sort_values(by=['id'], ascending=not sort_desc, inplace=True, ignore_index=True)
                elif sort_by == "description":
                    df.sort_values(by=['description'], ascending=not sort_desc,
                                   inplace=True, ignore_index=True)
                elif sort_by == "title":
                    df.sort_values(by=['title'], ascending=not sort_desc,
                                   inplace=True, ignore_index=True)
                elif sort_by == "publication_title":
                    df.sort_values(by=['publication_title'], ascending=not sort_desc,
                                   inplace=True, ignore_index=True)
                elif sort_by == "publication_location":
                    df.sort_values(by=['publication_location'], ascending=not sort_desc,
                                   inplace=True, ignore_index=True)
                elif sort_by == "type":
                    df.sort_values(by=['type'], ascending=not sort_desc, inplace=True, ignore_index=True)
                elif sort_by == "word_count":
                    df.sort_values(by=['word_count'], ascending=not sort_desc, inplace=True, ignore_index=True)
                else:
                    df.sort_values(by=['publication_date'], ascending=not sort_desc,
                                   inplace=True, ignore_index=True)
            else:
                df.sort_values(by=['id'], ascending=False, inplace=True, ignore_index=True)

            df = df.iloc[limit * page:limit * page + limit]
            total = len(df)

            for _, d in df.iterrows():
                d = d.where(pd.notnull(d), None)
                pub_date = datetime.strptime(d.publication_date, time_format) \
                    if isinstance(d.publication_date, str) else None
                load = {
                    'id': d["id"],
                    'source_id': d["source_id"],
                    'doc_title': d["doc_title"],
                    'pdf_location': d["pdf_location"],
                    'pdf_page_location': d["pdf_page_location"],
                    'ocr': d["ocr"],
                    'pdf_thumbnail_location': d["pdf_thumbnail_location"],
                    'candidate_document_id': d["candidate_document_id"],
                    'description': d["description"],
                    'publication_date': pub_date,
                    'publication_location': d["publication_location"],
                    'publication_title': d["publication_title"],
                    'type': d["type"],
                    'url': d["url"],
                    'word_count': d["word_count"],
                }
                docs.append(PortalDocument(**load))
    else:
        with session_scope() as session:
            docs_query = session.query(PortalDocument)
            if sort_by is not None and sort_by in ["id", "title", "publication_title", "publication_location",
                                                   "publication_date", "type", "word_count", "description"]:
                if sort_by == "id":
                    docs_query = docs_query.order_by(PortalDocument.id.desc()) if sort_desc \
                        else docs_query.order_by(PortalDocument.id)
                if sort_by == "description":
                    docs_query = docs_query.order_by(PortalDocument.description.desc()) if sort_desc \
                        else docs_query.order_by(PortalDocument.description)
                elif sort_by == "title":
                    docs_query = docs_query.order_by(PortalDocument.doc_title.desc()) if sort_desc \
                        else docs_query.order_by(PortalDocument.doc_title)
                elif sort_by == "publication_title":
                    docs_query = docs_query.order_by(PortalDocument.publication_title.desc()) if sort_desc \
                        else docs_query.order_by(PortalDocument.publication_title)
                elif sort_by == "publication_location":
                    docs_query = docs_query.order_by(PortalDocument.publication_location.desc()) if sort_desc \
                        else docs_query.order_by(PortalDocument.publication_location)
                elif sort_by == "type":
                    docs_query = docs_query.order_by(PortalDocument.type.desc()) if sort_desc \
                        else docs_query.order_by(PortalDocument.type)
                elif sort_by == "word_count":
                    docs_query = docs_query.order_by(PortalDocument.word_count.desc()) if sort_desc \
                        else docs_query.order_by(PortalDocument.word_count)
                else:
                    docs_query = docs_query.order_by(PortalDocument.publication_date.desc()) if sort_desc \
                        else docs_query.order_by(PortalDocument.publication_date)
            else:
                docs_query = docs_query.order_by(PortalDocument.id.desc())
            total = session.query(func.count(PortalDocument.id)).first()[0]
            docs = docs_query.limit(limit).offset(limit * page).all()
            session.expunge_all()
    docs = [r.to_dict() for r in docs]
    if not db_vars["local"]:
        for doc in docs:
            if doc["pdf_uri"] is not None and doc["pdf_uri"] != "":
                doc["pdf_uri"] = "https://coders.victorianelectionviolence.uk" + doc["pdf_uri"]
            if doc["cropped_pdf_uri"] is not None and doc["cropped_pdf_uri"] != "":
                doc["cropped_pdf_uri"] = "https://coders.victorianelectionviolence.uk" + doc["cropped_pdf_uri"]
    return docs, total


def get_total_portal_documents(db_vars):
    total = 0
    if db_vars["local"]:
        path = os.path.join(db_vars["data_dir"], f"{PortalDocument.__tablename__}.csv")
        if os.path.exists(path):
            total = len(pd.read_csv(path))
    else:
        with session_scope() as session:
            total = session.query(func.count(PortalDocument.id)).first()[0]
            session.expunge_all()
    return total
