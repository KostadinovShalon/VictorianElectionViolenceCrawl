from bs4 import BeautifulSoup
from Crawler.utils.databasemodels import CandidateDocument
from Crawler.utils import bna_login_utils as login, dbconn
from Crawler.utils.ocr import get_ocr_bna
import requests
from sqlalchemy import or_

payload = {
    'Username': login.username,
    "Password": login.password,
    "RememberMe": login.remember_me,
    "NextPage": login.next_page
}

documents = dbconn.session.query(CandidateDocument.id, CandidateDocument.url)\
                    .filter(or_(CandidateDocument.ocr == '',
                                CandidateDocument.ocr is None))\
                    .filter(or_(CandidateDocument.url.like('%britishnewspaper%'),
                                CandidateDocument.url.like('%wales')))\
                    .order_by(CandidateDocument.id).all()
wno_session = requests.Session()
bna_session = requests.Session()
payload = {
    'Username': login.username,
    "Password": login.password,
    "RememberMe": login.remember_me,
    "NextPage": login.next_page}
bna_session.post(login.login_url, data=payload, headers=login.headers)

n = len(documents)
print n, 'documents to update'

for document in documents:
    ocr = None
    if 'britishnewspaper' in document.url:
        ocr = get_ocr_bna(document.url, session=bna_session)
    elif 'wales' in document.url:
        html = wno_session.get(document.url)
        data = html.text
        soup = BeautifulSoup(data, "html.parser")
        get_id_detail = soup.find('div', attrs={'id': 'article-panel-main'})
        id_str = get_id_detail.script.get_text()
        id_str = id_str.split("'")[1]
        ocr = soup.find('div', attrs={'id': id_str}).find('span', attrs={'itemprop': 'articleBody'}).get_text()
    if ocr is not None:
        dbconn.session.query(CandidateDocument). \
            filter(CandidateDocument.id == document.id). \
            update(values={"ocr": ocr.encode('latin-1', 'ignore')})
        dbconn.session.commit()
        print 'Updated Candidate', document.id
