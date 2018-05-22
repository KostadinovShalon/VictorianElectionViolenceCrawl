from DB.databasemodels import ArchiveSearchResult, CandidateDocument
from DB import dbconn
import csv


def write_new_search_results(search_id, filename):
    unique_new_results = dbconn.session.query(ArchiveSearchResult.url).filter(ArchiveSearchResult.archive_search_id == search_id)
    for search_result in dbconn.session.query(ArchiveSearchResult)\
        .order_by(ArchiveSearchResult.id)\
            .filter(ArchiveSearchResult.archive_search_id == search_id)\
            .filter(~ArchiveSearchResult.url.in_(dbconn.session\
                                                 .query(CandidateDocument.url))):
        candidate_document = CandidateDocument(title=search_result.title,
                                           url=search_result.url,
                                           description=search_result.description,
                                           publication_title=search_result.publication_title,
                                           publication_location=search_result.publication_location,
                                           type=search_result.type,
                                           publication_date=search_result.publication_date,
                                           status="",
                                           word_count=search_result.word_count,
                                           page=search_result.page)
        dbconn.insert(candidate_document)

    needing_coding = dbconn.session.query(CandidateDocument.id, CandidateDocument.url, CandidateDocument.title,
                                          CandidateDocument.description, CandidateDocument.status, CandidateDocument.title)\
        .filter(CandidateDocument.url.in_(unique_new_results))\
        .filter(CandidateDocument.status != '0')\
            .filter(CandidateDocument.status != "1")
    with open("Crawler/Records/pending_" + filename + ".csv","wb") as f:
        fieldnames = ['candidate id', 'url','title', 'description','status', 'doc_title']
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        writer.writerows(needing_coding)

