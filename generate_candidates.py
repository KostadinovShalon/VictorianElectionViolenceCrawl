from Crawler.utils.dbutils import session_scope
from Crawler.utils.databasemodels import ArchiveSearchResult, CandidateDocument
import csv
import os

if os.path.exists('search_ids.csv'):
    with open('search_ids.csv', 'rb') as file_object:
        reader = csv.DictReader(file_object)
        searchs = [row for row in reader]
        for search in searchs:
            search_id = int(search['id'])
            filename = search['filename']
            with session_scope() as session:
                results = session.query(ArchiveSearchResult.url) \
                        .filter(ArchiveSearchResult.archive_search_id == search_id)
                needing_coding = session.query(CandidateDocument.id, CandidateDocument.url, CandidateDocument.title,
                                               CandidateDocument.description, CandidateDocument.status,
                                               CandidateDocument.g_status, CandidateDocument.title,
                                               CandidateDocument.status_writer) \
                    .filter(CandidateDocument.url.in_(results)) \
                    .filter(CandidateDocument.status != '0') \
                    .filter(CandidateDocument.status != "1")
                with open("Crawler/Records/" + filename + ".csv", "wb") as f:
                    fieldnames = ['id', 'url', 'publication_title', 'description', 'status',
                                  'g_status', 'title', 'status_writer']
                    writer = csv.writer(f)
                    writer.writerow(fieldnames)
                    writer.writerows(needing_coding)
else:
    print 'No search_ids.csv file found. You have to perform the crawler first'
