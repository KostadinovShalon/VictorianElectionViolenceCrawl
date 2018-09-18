from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean
from Crawler import Base


class ArchiveSearch(Base):
    __tablename__ = 'portal_archivesearch'
    id = Column(Integer, primary_key=True)
    archive = Column(String(30))
    search_text = Column(String(1000))
    archive_date_start = Column(String(100))
    archive_date_end = Column(String(100))
    search_batch_id = Column(String(30))
    added_date_end = Column(DateTime(6))
    added_date_start = Column(DateTime(6))
    article_type = Column(String(30))
    exact_phrase = Column(String(1000))
    exact_search = Column(Boolean)
    exclude_words = Column(String(1000))
    front_page = Column(Boolean)
    newspaper_title = Column(String(100))
    publication_place = Column(String(100))
    search_all_words = Column(String(1000))
    sort_by = Column(String(30))
    tags = Column(String(1000))
    timestamp = Column(DateTime(6))

    def __repr__(self):
        return "<Search (search text = '%s', start = '%s', end = '%s')>" % (
            self.search_text, self.archive_date_start, self.archive_date_end)


class ArchiveSearchResult(Base):
    __tablename__ = 'portal_archivesearchresult'
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    url = Column(String(1000))
    description = Column(String(10000))
    publication_title = Column(String(1000))
    publication_location = Column(String(100))
    type = Column(String(30))
    archive_search_id = Column(Integer, ForeignKey('portal_archivesearch.id'))
    publication_date = Column(Date)
    word_count = Column(Integer)

    def __repr__(self):
        return "<Search Result (title = '%s', type = '%s', date = '%s')>" % (
            self.title, self.type, self.publication_date)


class CandidateDocument(Base):
    __tablename__ = 'portal_candidatedocument'
    id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    url = Column(String(1000))
    description = Column(String(10000))
    publication_title = Column(String(1000))
    publication_location = Column(String(100))
    type = Column(String(30))
    status = Column(String(30))
    page = Column(Integer)
    publication_date = Column(Date)
    word_count = Column(Integer)
    ocr = Column(String)
    g_status = Column(String(30))
    status_writer = Column(String(30))


class PortalDocument(Base):
    __tablename__ = 'portal_document'
    id = Column(Integer, primary_key=True)
    source_id = Column(String(30))
    doc_title = Column(String(100))
    pdf_location = Column(String(300))
    pdf_page_location = Column(String(300))
    ocr = Column(String)
    pdf_thumbnail_location = Column(String(300))
    candidate_document_id = Column(Integer, ForeignKey('portal_candidatedocument.id'))
    description = Column(String(10000))
    publication_date = Column(Date)
    publication_location = Column(String(100))
    publication_title = Column(String(1000))
    type = Column(String(30))
    url = Column(String(1000))
    word_count = Column(Integer)
    page = 0
