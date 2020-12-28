import requests

from Crawler.utils import bna_login_url, headers
from db.dbconn import update_candidate, insert, update_art_url, update_page_url
from db.db_session import session_scope
from FilesHandler.BNAHandler import BNAHandler
from db.databasemodels import PortalDocument, CandidateDocument
from Crawler.utils.ocr import get_ocr_bna
import configuration


class CandidateDownloader:

    def __init__(self, articles):
        self.processing_article_index = 0  # Current article being processed [from 1 to N]
        self.processed_articles = []  # List of tuples with the candidate id and the processed results
        self.status = (0, "Initializing")
        # for art in articles:
        #     if art["g_status"] is None or art["g_status"] == "":
        #         art["g_status"] = art["status"]
        #     if art["status_writer"] is None:
        #         art["status_writer"] = ''
        for art in articles:
            art["g_status"] = str(art["status"])
            art["status_writer"] = ''  # For Now TODO: Change to actual writer
        self.articles_to_process = [art for art in articles if str(art["status"]) == "1"]  # Articles with status = 1
        self.total_portal_articles = len(self.articles_to_process)  # Number of articles with status = 1
        self.other_articles = [art for art in articles if str(art["status"]) != "1"]  # Articles with status != 1
        self.login_details = configuration.get_login_details()
        self.bna_handlers = {article["id"]: BNAHandler(article["id"], self.login_details)
                             for article in self.articles_to_process}
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def update_and_download_candidates(self):
        if self._cancel:
            return
        self.status = 1, "Updating article status different than 1"
        with session_scope() as session:
            for article in self.other_articles:
                update_candidate(session, article["id"], str(article["status"]),
                                 article["g_status"], article["status_writer"])
        login_details = configuration.get_login_details()
        s = requests.Session()
        payload = {
            'Username': login_details["username"],
            "Password": login_details["password"],
            "RememberMe": login_details["remember_me"],
            "NextPage": login_details["next_page"]}
        s.post(bna_login_url, data=payload, headers=headers)
        if self._cancel:
            return

        for i, article in enumerate(self.articles_to_process):
            if self._cancel:
                return
            self.processing_article_index = i + 1
            candidate_id = article["id"]
            article_status = article["status"]
            g_status = article["g_status"]
            status_writer = article["status_writer"]

            with session_scope() as session:
                candidate_document = session.query(CandidateDocument) \
                    .filter(CandidateDocument.id == candidate_id).first()
                publication_date = candidate_document.publication_date
                title = candidate_document.title
                county = candidate_document.publication_location
                description_article = candidate_document.description
                download_page = candidate_document.url
                newspaper = candidate_document.publication_title
                type_ = candidate_document.type
                words = candidate_document.word_count
            self.status = 2, f"Processing Article {candidate_id}: {title}"

            file_processed = False
            art_uploaded = False
            ocr = None

            if len(title) > 100:
                title = title[:100]
            doc_title = title
            des = description_article

            check_if_exists = session.query(PortalDocument.id) \
                .filter(PortalDocument.ocr == ocr) \
                .filter(PortalDocument.url == download_page).all()

            publication_date = '{0.year:4d}-{0.month:02d}-{0.day:02d}'.format(publication_date)
            if len(check_if_exists) == 0:
                document = PortalDocument(source_id="2", doc_title=doc_title,
                                          pdf_location="", pdf_page_location="",
                                          ocr=ocr,
                                          pdf_thumbnail_location="No", candidate_document_id=candidate_id,
                                          description=des,
                                          publication_date=publication_date,
                                          publication_location=county,
                                          publication_title=newspaper,
                                          type=type_,
                                          url=download_page, word_count=words)

                with session_scope() as session:
                    try:
                        handler = self.bna_handlers[candidate_id]
                        if document.ocr is None or document.ocr == '':
                            ocr = get_ocr_bna(download_page, login_details, session=s)
                            document.ocr = ocr.encode('latin-1', 'ignore')
                        if self._cancel:
                            return
                        insert(session, document)
                        update_candidate(session, candidate_id, str(article_status), g_status, status_writer)
                        file_processed = True
                        self.status = 3, f"Processing Article {candidate_id} (Downloading article): {title}"
                        handler.download_full_pages(s)
                        self.status = 4, f"Processing Article {candidate_id} (Uploading full article): {title}"
                        if self._cancel:
                            return
                        handler.upload_full_pages(document.id)
                        if self._cancel:
                            return
                        self.status = 5, f"Processing Article {candidate_id} (Cropping article): {title}"
                        handler.create_cropped_image()
                        if self._cancel:
                            return
                        self.status = 6, f"Processing Article {candidate_id} (Uploading cropped article): {title}"
                        if self._cancel:
                            return
                        handler.upload_cropped_pages(document.id)
                        art_uploaded = True
                    except Exception as e:
                        print(e)
                    if file_processed:
                        if art_uploaded:
                            if self._cancel:
                                return
                            update_page_url(session, document.id, f"/static/documents/{document.id}/page.pdf")
                            update_art_url(session, document.id, f"/static/documents/{document.id}/art.pdf")
                            self.processed_articles.append((candidate_id, "Portal document inserted"))
                        else:
                            self.processed_articles.append((candidate_id, "Portal document inserted without uploading"))
                    else:
                        self.processed_articles.append((candidate_id, "Portal document not inserted"))
            else:
                if self._cancel:
                    return
                update_candidate(session, candidate_id, '101', g_status, status_writer)
                self.processed_articles.append((candidate_id,
                                                f"Article not inserted. "
                                                f"An identical article was found at id = {check_if_exists[0].id}. "
                                                f"Updating status to 101"))

    def flush_files(self):
        self.status = 7, f"Flushing articles in local machine"
        for h in self.bna_handlers.values():
            h.flush()
