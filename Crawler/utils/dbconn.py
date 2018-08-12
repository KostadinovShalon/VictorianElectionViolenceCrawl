from datetime import datetime
from Crawler.utils.databasemodels import CandidateDocument, PortalDocument


def insert_search(session, archive_search):
    archive_search.timestamp = datetime.now()
    session.add(archive_search)
    session.commit()


def insert(session, archive_to_insert):
    session.add(archive_to_insert)
    session.commit()


def update_candidate(session, candidate_id, status):
    session.query(CandidateDocument). \
        filter(CandidateDocument.id == candidate_id). \
        update(values={"status": status})
    session.commit()


def update_page_url(session, document_id, page_url):
    try:
        session.query(PortalDocument). \
            filter(PortalDocument.id == document_id). \
            update(values={"pdf_page_location": page_url})
        session.commit()
    except:
        session.rollback()


def update_art_url(session, document_id, pdf_url):
    session.query(PortalDocument). \
        filter(PortalDocument.id == document_id). \
        update(values={"pdf_location": pdf_url})
    session.commit()
