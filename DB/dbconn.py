from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from DB import databasemodels
from DB.databasemodels import CandidateDocument, PortalDocument

engine = create_engine('mysql+mysqldb://data_feeder:Arp48dEx@coders.victorianelectionviolence.uk/evp')
databasemodels.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def insert_search(archive_search):
    archive_search.timestamp = datetime.now()
    session.add(archive_search)
    session.commit()


def insert(archive_to_insert):
    session.add(archive_to_insert)
    session.commit()


def update_candidate(candidate_id, status):
    session.query(CandidateDocument). \
        filter(CandidateDocument.id == candidate_id). \
        update(values={"status": status})
    session.commit()

def update_page_url(document_id, page_url):
    session.query(PortalDocument). \
        filter(PortalDocument.id == document_id). \
        update(values={"pdf_page_location": page_url})
    session.commit()

def update_art_url(document_id, pdf_url):
    session.query(PortalDocument). \
        filter(PortalDocument.id == document_id). \
        update(values={"pdf_location": pdf_url})
    session.commit()
