import requests
from bs4 import BeautifulSoup

import configuration
from Crawler.utils.ocr import get_ocr_bna
from db.databasemodels import CandidateDocument
from db.db_session import session_scope


def update_ocr(candidate_id):
    login_details = configuration.get_login_details()
    payload = {
        'Username': login_details["username"],
        "Password": login_details["password"],
        "RememberMe": login_details["remember_me"],
        "NextPage": login_details["next_page"]
    }
    with session_scope() as session:
        document = session.query(CandidateDocument.url) \
            .filter(CandidateDocument.id == candidate_id).first()
        bna_session = requests.Session()
        bna_session.post(login_details["login_url"], data=payload, headers=login_details["headers"])

        ocr = None
        if 'britishnewspaper' in document.url:
            ocr = get_ocr_bna(document.url, session=bna_session)
        if ocr is not None:
            session.query(CandidateDocument). \
                filter(CandidateDocument.id == candidate_id). \
                update(values={"ocr": ocr.encode('latin-1', 'ignore')})
            session.commit()
    return ocr
