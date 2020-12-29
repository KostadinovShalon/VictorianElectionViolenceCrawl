import requests

import configuration
from Crawler.utils import bna_login_url, headers
from FilesHandler.BNAHandler import BNAHandler
from db.databasemodels import PortalDocument
from db.db_session import session_scope
from db.dbconn import update_art_url, update_page_url


class PortalDocumentsUpdater:

    def __init__(self, document_id):
        self.status = (0, "Initializing")
        self.login_details = configuration.get_login_details()
        with session_scope() as session:
            result = session.query(PortalDocument.candidate_document_id) \
                .filter(PortalDocument.id == document_id).first()
            self.bna_handler = BNAHandler(result.candidate_document_id, self.login_details)
        self.document_id = document_id
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def update_documents(self):
        if self._cancel:
            return
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

        with session_scope() as session:
            try:
                self.status = 1, f"Downloading article"
                self.bna_handler.download_full_pages(s)
                self.status = 2, f"Uploading full article"
                if self._cancel:
                    return
                self.bna_handler.upload_full_pages(self.document_id)
                update_page_url(session, self.document_id, f"/static/documents/{self.document_id}/page.pdf")
                if self._cancel:
                    return
                self.status = 3, f"Cropping article"
                self.bna_handler.create_cropped_image()
                if self._cancel:
                    return
                self.status = 4, f"Uploading cropped article"
                if self._cancel:
                    return
                self.bna_handler.upload_cropped_pages(self.document_id)
                update_art_url(session, self.document_id, f"/static/documents/{self.document_id}/art.pdf")
            except Exception as e:
                print(e)

    def flush_files(self):
        self.status = 7, f"Flushing articles in local machine"
        self.bna_handler.flush()
