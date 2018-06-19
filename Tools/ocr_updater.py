import sys
import os

from bs4 import BeautifulSoup

sys.path.append(os.path.abspath('..'))
from DB import dbconn
from DB.databasemodels import CandidateDocument
import requests
import json

LOGIN_PAGE = "https://www.britishnewspaperarchive.co.uk/account/login"

payload = {
'Username': "nick.vivyan@durham.ac.uk",
"Password": "EV19@Nick",
"RememberMe": "false",
"NextPage": ""}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.britishnewspaperarchive.co.uk",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
    "Origin": "https://www.britishnewspaperarchive.co.uk",
    "Link": "<https://www.britishnewspaperarchive.co.uk/account/login>; rel=\"canonical\"",
    "X-Frame-Options": "SAMEORIGIN"
}

documents = dbconn.session.query(CandidateDocument.id, CandidateDocument.url).\
                    filter(CandidateDocument.url.like('%wales%')).\
                    order_by(CandidateDocument.id).all()
s = requests.Session()
#s.post(LOGIN_PAGE, data=payload, headers=headers)

n = len(documents)
c = 0

# for document in documents:
#     link = document.url.split('bl')[1]
#     ocr_link = 'https://www.britishnewspaperarchive.co.uk/tags/itemocr/BL/' + link
#     json_str = s.get(ocr_link)
#     json_str.encoding = 'gbk'
#     json_str = json.loads(json_str.content)
#     OCR_text = ''
#     for j in json_str:
#         OCR_text = OCR_text + j['LineText']
#     dbconn.session.query(CandidateDocument). \
#         filter(CandidateDocument.id == document.id). \
#         update(values={"ocr": OCR_text.encode('latin-1', 'ignore')})
#     dbconn.session.commit()
#     c += 1
#     print 'Updated: ' + str(100*(float(c) / n))

for document in documents:
    html = s.get(document.url)
    data = html.text
    soup = BeautifulSoup(data, "html.parser")
    get_id_detail = soup.find('div', attrs={'id': 'article-panel-main'})
    id_str = get_id_detail.script.get_text()
    id_str = id_str.split("'")[1]
    this_OCR = soup.find('div', attrs={'id': id_str}).find('span', attrs={'itemprop': 'articleBody'}).get_text()
    dbconn.session.query(CandidateDocument). \
         filter(CandidateDocument.id == document.id). \
         update(values={"ocr": this_OCR.encode('latin-1', 'ignore')})
    dbconn.session.commit()
    c += 1
    print 'Updated: ' + str(100*(float(c) / n))