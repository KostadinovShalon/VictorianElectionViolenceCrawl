from Crawler.utils.databasemodels import PortalDocument
from FilesHandler.BNAHandler import BNAHandler
from Crawler.utils.dbutils import session_scope
import tqdm

with session_scope() as session:
    documents = session.query(PortalDocument.id, PortalDocument.url).\
                        filter(PortalDocument.url.like('%britishnewspaperarchive%')).\
                        filter(PortalDocument.id > 154).filter(PortalDocument.id < 208).\
                        order_by(PortalDocument.id).all()

    for document in tqdm.tqdm(documents):
        url = document.url.replace('viewer', 'viewer/items')
        handler = BNAHandler(url)
        print("Downloading article")
        try:
            article_file = handler.download_and_upload_file(document.id)
        except:
            article_file = handler.download_and_upload_file(document.id)
        print("Article downloaded and uploaded to the server")
