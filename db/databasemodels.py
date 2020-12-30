from sqlalchemy import Column, Integer, DateTime, Date, ForeignKey, Boolean, Unicode, UnicodeText
from db.db_session import Base
import pandas as pd

collation = 'latin1_swedish_ci'


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
    archive = Column(Unicode(30))
    search_text = Column(Unicode(1000, collation=collation))
    archive_date_start = Column(Unicode(100, collation=collation))
    archive_date_end = Column(Unicode(100, collation=collation))
    search_batch_id = Column(Unicode(30, collation=collation))
    added_date_end = Column(DateTime(6))
    added_date_start = Column(DateTime(6))
    article_type = Column(Unicode(30, collation=collation))
    exact_phrase = Column(Unicode(1000, collation=collation))
    exact_search = Column(Boolean)
    exclude_words = Column(Unicode(1000, collation=collation))
    front_page = Column(Boolean)
    newspaper_title = Column(Unicode(100, collation=collation))
    publication_place = Column(Unicode(100, collation=collation))
    search_all_words = Column(Unicode(1000, collation=collation))
    sort_by = Column(Unicode(30, collation=collation))
    tags = Column(Unicode(1000, collation=collation))
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

    def to_data_frame(self):
        return pd.DataFrame({
            'id': [self.id],
            'archive': [self.archive],
            'search_text': [self.search_text],
            'archive_date_start': [self.archive_date_start],
            'archive_date_end': [self.archive_date_end],
            'search_batch_id': [self.search_batch_id],
            'added_date_end': [self.added_date_end],
            'added_date_start': [self.added_date_start],
            'article_type': [self.article_type],
            'exact_phrase': [self.exact_phrase],
            'exact_search': [self.exact_search],
            'exclude_words': [self.exclude_words],
            'front_page': [self.front_page],
            'newspaper_title': [self.newspaper_title],
            'publication_place': [self.publication_place],
            'search_all_words': [self.search_all_words],
            'sort_by': [self.sort_by],
            'tags': [self.tags],
            'timestamp': [dump_datetime(self.timestamp)],
        })


class ArchiveSearchCount(Base):
    __tablename__ = 'portal_archivesearchsummaryonly'
    id = Column(Integer, primary_key=True)
    archive = Column(Unicode(30, collation=collation))
    search_text = Column(Unicode(1000, collation=collation))
    archive_date_start = Column(Unicode(100, collation=collation))
    archive_date_end = Column(Unicode(100, collation=collation))
    search_batch_id = Column(Unicode(30, collation=collation))
    added_date_end = Column(DateTime(6))
    added_date_start = Column(DateTime(6))
    article_type = Column(Unicode(30, collation=collation))
    exact_phrase = Column(Unicode(1000, collation=collation))
    exact_search = Column(Boolean)
    exclude_words = Column(Unicode(1000, collation=collation))
    front_page = Column(Boolean)
    newspaper_title = Column(Unicode(100, collation=collation))
    publication_place = Column(Unicode(100, collation=collation))
    search_all_words = Column(Unicode(1000, collation=collation))
    sort_by = Column(Unicode(30, collation=collation))
    tags = Column(Unicode(1000, collation=collation))
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

    def to_data_frame(self):
        return pd.DataFrame({
            'id': [self.id],
            'archive': [self.archive],
            'search_text': [self.search_text],
            'archive_date_start': [self.archive_date_start],
            'archive_date_end': [self.archive_date_end],
            'search_batch_id': [self.search_batch_id],
            'added_date_end': [self.added_date_end],
            'added_date_start': [self.added_date_start],
            'article_type': [self.article_type],
            'exact_phrase': [self.exact_phrase],
            'exact_search': [self.exact_search],
            'exclude_words': [self.exclude_words],
            'front_page': [self.front_page],
            'newspaper_title': [self.newspaper_title],
            'publication_place': [self.publication_place],
            'search_all_words': [self.search_all_words],
            'sort_by': [self.sort_by],
            'tags': [self.tags],
            'timestamp': [dump_datetime(self.timestamp)],
            'results_count': [self.results_count]
        })


class ArchiveSearchResult(Base):
    __tablename__ = 'portal_archivesearchresult'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(1000, collation=collation))
    url = Column(Unicode(1000, collation=collation))
    description = Column(Unicode(10000, collation=collation))
    publication_title = Column(Unicode(1000, collation=collation))
    publication_location = Column(Unicode(100, collation=collation))
    type = Column(Unicode(30, collation=collation))
    archive_search_id = Column(Integer, ForeignKey('portal_archivesearch.id'))
    publication_date = Column(Date)
    word_count = Column(Integer)

    def __repr__(self):
        return "<Search Result (title = '%s', type = '%s', date = '%s')>" % (
            self.title, self.type, self.publication_date)

    def to_data_frame(self):
        return pd.DataFrame({
            'id': [self.id],
            'title': [self.title],
            'url': [self.url],
            'description': [self.description],
            'publication_title': [self.publication_title],
            'publication_location': [self.publication_location],
            'type': [self.type],
            'archive_search_id': [self.archive_search_id],
            'publication_date': [self.publication_date],
            'word_count': [self.word_count]
        })


class CandidateDocument(Base):
    __tablename__ = 'portal_candidatedocument'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(1000, collation=collation))
    url = Column(Unicode(1000, collation=collation))
    description = Column(Unicode(10000, collation=collation))
    publication_title = Column(Unicode(1000, collation=collation))
    publication_location = Column(Unicode(100, collation=collation))
    type = Column(Unicode(30, collation=collation))
    status = Column(Unicode(30, collation=collation))
    page = Column(Integer)
    publication_date = Column(Date)
    word_count = Column(Integer)
    ocr = Column(Unicode(100000, collation=collation))
    g_status = Column(Unicode(30, collation=collation))
    status_writer = Column(Unicode(30, collation=collation))

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

    def to_data_frame(self):
        return pd.DataFrame({
            'id': [self.id],
            'title': [self.title],
            'url': [self.url],
            'description': [self.description],
            'publication_title': [self.publication_title],
            'publication_location': [self.publication_location],
            'type': [self.type],
            'status': [self.status],
            'page': [self.page],
            'publication_date': [self.publication_date],
            'word_count': [self.word_count],
            'ocr': [self.ocr],
            'g_status': [self.g_status],
            'status_writer': [self.status_writer]
        })


class PortalDocument(Base):
    __tablename__ = 'portal_document'
    id = Column(Integer, primary_key=True)
    source_id = Column(Unicode(30, collation=collation))
    doc_title = Column(Unicode(100, collation=collation))
    pdf_location = Column(Unicode(300, collation=collation))
    pdf_page_location = Column(Unicode(300, collation=collation))
    ocr = Column(UnicodeText(collation=collation))
    pdf_thumbnail_location = Column(Unicode(300, collation=collation))
    candidate_document_id = Column(Integer, ForeignKey('portal_candidatedocument.id'))
    description = Column(Unicode(10000, collation=collation))
    publication_date = Column(Date)
    publication_location = Column(Unicode(100, collation=collation))
    publication_title = Column(Unicode(1000, collation=collation))
    type = Column(Unicode(30, collation=collation))
    url = Column(Unicode(1000, collation=collation))
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

    def to_data_frame(self):
        return pd.DataFrame({
            'id': [self.id],
            'source_id': [self.source_id],
            'doc_title': [self.doc_title],
            'pdf_location': [self.pdf_location],
            'pdf_page_location': [self.pdf_page_location],
            'ocr': [self.ocr],
            'pdf_thumbnail_location': [self.pdf_thumbnail_location],
            'candidate_document_id': [self.candidate_document_id],
            'description': [self.description],
            'publication_date': [self.publication_date],
            'publication_location': [self.publication_location],
            'publication_title': [self.publication_title],
            'type': [self.type],
            'url': [self.url],
            'word_count': [self.word_count],
        })
