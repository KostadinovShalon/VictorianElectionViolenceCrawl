import requests
from Crawler.utils import bna_login_utils as login
import json


def get_ocr_bna(url, cookies=None, session=None):
    link = url.split('bl')[1]
    ocr_text = ''
    ocr_link = 'https://www.britishnewspaperarchive.co.uk/tags/itemocr/BL/' + link

    if session is not None:
        json_str = session.get(ocr_link, headers=login.headers)
    elif cookies is not None:
        json_str = requests.get(ocr_link, headers=login.headers, cookies=cookies)
    else:
        s = requests.Session()
        payload = {
            'Username': login.username,
            "Password": login.password,
            "RememberMe": login.remember_me,
            "NextPage": login.next_page}
        s.post(login.login_url, data=payload, headers=login.headers)
        json_str = s.get(ocr_link, headers=login.headers)
    json_str.encoding = 'gbk'
    json_str = json.loads(json_str.content)
    for j in json_str:
        ocr_text = ocr_text + j['LineText']
    return ocr_text
