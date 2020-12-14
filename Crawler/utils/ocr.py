import requests
import json
from Crawler.utils import headers, bna_login_url


def get_ocr_bna(url, login_details, cookies=None, session=None):
    link = url.split('bl')[1]
    ocr_text = ''
    ocr_link = 'https://www.britishnewspaperarchive.co.uk/tags/itemocr/BL/' + link

    if session is not None:
        json_str = session.get(ocr_link, headers=headers)
    elif cookies is not None:
        json_str = requests.get(ocr_link, headers=headers, cookies=cookies)
    else:
        s = requests.Session()
        payload = {
            'Username': login_details["username"],
            "Password": login_details["password"],
            "RememberMe": login_details["remember_me"],
            "NextPage": login_details["next_page"]}
        s.post(bna_login_url, data=payload, headers=headers)
        json_str = s.get(ocr_link, headers=headers)
    json_str.encoding = 'gbk'
    try:
        json_str = json.loads(json_str.content)
        for j in json_str:
            ocr_text = ocr_text + j['LineText']
        return ocr_text
    except ValueError:
        return None
