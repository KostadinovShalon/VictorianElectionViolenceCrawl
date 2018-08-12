from Crawler.utils import dbconn
from Crawler.utils.databasemodels import PortalDocument
from FilesHandler.BNAHandler import BNAHandler

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
