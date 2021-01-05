import requests

from Crawler.utils import bna_login_url, headers
from FilesHandler.BNAHandler import BNAHandler
from repositories.portal_documents_repo import get_portal_document, update_portal_page_url, update_portal_cropped_url


class PortalDocumentsUpdater:

    def __init__(self, document_id, login_details, server_details, db_vars):
        self.status = (0, "Initializing")
        self.login_details = login_details
        document = get_portal_document(document_id, db_vars)
        self.bna_handler = BNAHandler(document.candidate_document_id, self.login_details, server_details, db_vars)
        self.document_id = document_id
        self._cancel = False
        self.db_vars = db_vars

    def cancel(self):
        self._cancel = True

    def update_documents(self):
        if self._cancel:
            return
        s = requests.Session()
        payload = {
            'Username': self.login_details["username"],
            "Password": self.login_details["password"],
            "RememberMe": self.login_details["remember_me"],
            "NextPage": self.login_details["next_page"]}
        s.post(bna_login_url, data=payload, headers=headers)
        if self._cancel:
            return

        try:
            self.status = 1, f"Downloading article"
            self.bna_handler.download_full_pages(s)
            self.status = 2, f"Uploading full article"
            if self._cancel:
                return
            self.bna_handler.upload_full_pages(self.document_id)
            update_portal_page_url(self.document_id, self.db_vars, self.bna_handler.temp_full_file_pdf_name)
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
            update_portal_cropped_url(self.document_id, self.db_vars, self.bna_handler.temp_cropped_file_pdf_name)
        except Exception as e:
            print(e)

    def flush_files(self):
        self.status = 7, f"Flushing articles in local machine"
        self.bna_handler.flush()
