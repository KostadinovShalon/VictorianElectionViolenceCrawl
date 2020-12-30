import requests

import configuration
from Crawler.utils.ocr import get_ocr_bna
from repositories.candidates_repo import get_candidate, update_candidate_ocr


def update_ocr(candidate_id):
    login_details = configuration.get_login_details()
    payload = {
        'Username': login_details["username"],
        "Password": login_details["password"],
        "RememberMe": login_details["remember_me"],
        "NextPage": login_details["next_page"]
    }
    bna_session = requests.Session()
    bna_session.post(login_details["login_url"], data=payload, headers=login_details["headers"])

    ocr = None
    document = get_candidate(candidate_id)
    if 'britishnewspaper' in document.url:
        ocr = get_ocr_bna(document.url, session=bna_session)
    if ocr is not None:
        update_candidate_ocr(candidate_id, ocr.encode('utf8', 'replace').decode('cp1252', 'ignore'))
    return ocr
