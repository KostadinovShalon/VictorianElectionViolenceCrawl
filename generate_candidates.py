from Crawler.utils.dbutils import session_scope
from Crawler.utils.databasemodels import ArchiveSearchResult, CandidateDocument
from Crawler.utils.dbconn import insert
import csv
import json
import os

if os.path.exists('search_ids.csv'):
    with open('search_ids.csv', 'rb') as file_object:
        reader = csv.DictReader(file_object)
        searchs = [row for row in reader]
        for search in searchs:
            search_id = int(search['id'])
            filename = search['filename']
            with session_scope() as session:
                unique_new_results = session.query(ArchiveSearchResult.url) \
                        .filter(ArchiveSearchResult.archive_search_id == search_id)
                for search_result in session.query(ArchiveSearchResult) \
                        .order_by(ArchiveSearchResult.id) \
                        .filter(ArchiveSearchResult.archive_search_id == search_id) \
                        .filter(~ArchiveSearchResult.url.in_(session.query(CandidateDocument.url))):
                    full_json_path = "Crawler/Records/" + filename + ".json"
                    ocr = ""
                    page = 0
                    try:
                        with open(full_json_path, 'rb') as json_file:
                            info = json_file.read()
                            info = info.strip()
                            info = "[" + info[:-1] + "]"
                            jarray = json.loads(info)
                            jarticle = next((row for row in jarray if row['download_url'] == search_result.url), None)
                            if jarticle is None:
                                jarticle = next((row for row in jarray if row['download_page'] == search_result.url),
                                                None)
                            if jarticle is not None:
                                ocr = jarticle["ocr"]
                                page = int(jarticle["page"])
                    except:
                        if 'britishnewspaper' in search_result.url:
                            page = int(search_result.url.split('/')[-1])
                    candidate_document = CandidateDocument(title=search_result.title,
                                                           url=search_result.url,
                                                           description=search_result.description,
                                                           publication_title=search_result.publication_title,
                                                           publication_location=search_result.publication_location,
                                                           type=search_result.type,
                                                           publication_date=search_result.publication_date,
                                                           status="", g_status="", status_writer="gary",
                                                           word_count=search_result.word_count,
                                                           page=page,
                                                           ocr=ocr.encode('latin-1', 'ignore'))
                    insert(session, candidate_document)

                needing_coding = session.query(CandidateDocument.id, CandidateDocument.url, CandidateDocument.title,
                                               CandidateDocument.description, CandidateDocument.status,
                                               CandidateDocument.g_status, CandidateDocument.title,
                                               CandidateDocument.status_writer) \
                    .filter(CandidateDocument.url.in_(unique_new_results)) \
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
