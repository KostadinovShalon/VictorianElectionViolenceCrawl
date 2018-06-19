import sys
import os
sys.path.append(os.path.abspath('..'))
from DB import dbconn
from DB.databasemodels import PortalDocument
from FilesHandler.BNAHandler import BNAHandler
import requests


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

documents = dbconn.session.query(PortalDocument.id, PortalDocument.url).\
                    filter(PortalDocument.url.like('%britishnewspaperarchive%')).\
                    filter(PortalDocument.id > 154).filter(PortalDocument.id < 208).\
                    order_by(PortalDocument.id).all()

n = len(documents)
c = 0

for document in documents:
    url = document.url.replace('viewer', 'viewer/items')
    handler = BNAHandler(url)
    print "Downloading article"
    try:
        article_file = handler.download_and_upload_file(document.id)
    except:
        article_file = handler.download_and_upload_file(document.id)
    print "Article downloaded and uploaded to the server"
    c += 1
    print 'Updated: ' + str(100 * (float(c) / n))
