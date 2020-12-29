from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean
from db.db_session import Base


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")


def dump_date(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")


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

    def to_dict(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'keyword': self.search_text,
            'start_date': self.archive_date_start,
            'end_date': self.archive_date_end,
            'archive': self.search_batch_id,
            'added_date_end': self.added_date_end,
            'added_date_start': self.added_date_start,
            'article_type': self.article_type,
            'exact_phrase': self.exact_phrase,
            'exact_search': self.exact_search,
            'exclude_words': self.exclude_words,
            'front_page': self.front_page,
            'newspaper_title': self.newspaper_title,
            'publication_place': self.publication_place,
            'search_all_words': self.search_all_words,
            'sort_by': self.sort_by,
            'tags': self.tags,
            'timestamp': dump_datetime(self.timestamp),
        }


class ArchiveSearchCount(Base):
    __tablename__ = 'portal_archivesearchsummaryonly'
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
    results_count = Column(Integer)

    def __repr__(self):
        return "<Search (search text = '%s', start = '%s', end = '%s', count='%d')>" % (
            self.search_text, self.archive_date_start, self.archive_date_end, self.results_count)

    def to_dict(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'keyword': self.search_text,
            'start_date': self.archive_date_start,
            'end_date': self.archive_date_end,
            'archive': self.search_batch_id,
            'added_date_end': self.added_date_end,
            'added_date_start': self.added_date_start,
            'article_type': self.article_type,
            'exact_phrase': self.exact_phrase,
            'exact_search': self.exact_search,
            'exclude_words': self.exclude_words,
            'front_page': self.front_page,
            'newspaper_title': self.newspaper_title,
            'publication_place': self.publication_place,
            'search_all_words': self.search_all_words,
            'sort_by': self.sort_by,
            'tags': self.tags,
            'timestamp': dump_datetime(self.timestamp),
            'count': self.results_count
        }


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
    ocr = Column(String(100000))
    g_status = Column(String(30))
    status_writer = Column(String(30))

    def to_dict(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'description': self.description,
            'publication_title': self.publication_title,
            'publication_location': self.publication_location,
            'type': self.type,
            'status': self.status,
            'page': self.page,
            'publication_date': dump_date(self.publication_date),
            'word_count': self.word_count,
            'ocr': self.ocr,
            'g_status': self.g_status,
            'status_writer': self.status_writer
        }


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

    def to_dict(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'title': self.doc_title,
            'pdf_uri': self.pdf_page_location,
            'cropped_pdf_uri': self.pdf_location,
            'url': self.url,
            'description': self.description,
            'publication_title': self.publication_title,
            'publication_location': self.publication_location,
            'type': self.type,
            'publication_date': dump_date(self.publication_date),
            'word_count': self.word_count,
            'ocr': self.ocr,
        }
