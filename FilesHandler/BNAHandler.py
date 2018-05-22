from io import BytesIO
from FileHandler import upload_file
import requests


class BNAHandler:

    LOGIN_PAGE = "https://www.britishnewspaperarchive.co.uk/account/login"

    payload = {
        'Username': "nick.vivyan@durham.ac.uk",
        "Password": "EV19@Nick",
        "RememberMe": "false",
        "NextPage": ""}

    headers = {
        "Accept"            :"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding"   :"gzip, deflate, br",
        "Accept-Language"   :"zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control"     :"max-age=0",
        "Connection"        :"keep-alive",
        "Host"              :"www.britishnewspaperarchive.co.uk",
        "User-Agent"        :"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
        "Origin"            :"https://www.britishnewspaperarchive.co.uk",
        "Link"              :"<https://www.britishnewspaperarchive.co.uk/account/login>; rel=\"canonical\"",
        "X-Frame-Options"   :"SAMEORIGIN"
        }
    s = requests.Session()
    s.post(LOGIN_PAGE, data=payload, headers=headers)

    def __init__(self):
        pass

    def get_dim(self, item_url):
        resp = self.s.get(item_url)
        j = resp.json()
        return j["Items"]

    def download_and_upload_file(self, article_url, document_id):
        f = self.s.get(article_url)
        tmp = BytesIO(f.content)
        tmp.seek(0)
        upload_file(document_id, tmp, "page.pdf")
        return tmp

