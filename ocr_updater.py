from bs4 import BeautifulSoup
from db import CandidateDocument
from Crawler.utils import bna_login_utils as login
from Crawler.utils import get_ocr_bna
import requests
from sqlalchemy import or_
from db import session_scope
import csv

payload = {
    'Username': login.username,
    "Password": login.password,
    "RememberMe": login.remember_me,
    "NextPage": login.next_page}

f = input('CSV Filename with candidates whose OCR is going to be downloaded'
          ' (without extension): ')
csv_path = f + ".csv"
candidates = []
with open(csv_path, 'rb') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    print("Reading", csv_path)
    try:
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
            else:
                try:
                    candidates.append(row[0])
                except ValueError as e:
                    print(e)
    except csv.Error:
        print("File does not exists")
with session_scope() as session:
    documents = session.query(CandidateDocument.id, CandidateDocument.url) \
        .filter(or_(CandidateDocument.ocr == '',
                    CandidateDocument.ocr is None)) \
        .filter(or_(CandidateDocument.url.like('%britishnewspaper%'),
                    CandidateDocument.url.like('%wales'))) \
        .filter(CandidateDocument.id.in_(tuple(candidates))) \
        .order_by(CandidateDocument.id).all()
    wno_session = requests.Session()
    bna_session = requests.Session()
    bna_session.post(login.login_url, data=payload, headers=login.headers)

    n = len(documents)
    print(n, 'documents to update')

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
            session.query(CandidateDocument). \
                filter(CandidateDocument.id == document.id). \
                update(values={"ocr": ocr.encode('latin-1', 'ignore')})
            session.commit()
            print('Updated Candidate', document.id)
