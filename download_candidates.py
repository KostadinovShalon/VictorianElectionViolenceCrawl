import csv
import json
from Crawler.utils.dbconn import update_candidate, insert, update_art_url, update_page_url
from Crawler.utils.dbutils import session_scope
from FilesHandler.BNAHandler import BNAHandler
from Crawler.utils.databasemodels import PortalDocument, CandidateDocument
import datetime
import os.path
from Crawler.utils.ocr import get_ocr_bna

f = input('CSV Filename (without extension): ')

high_resolution = False
if "britishnewspaperarchive" in f:
    tag = "BNA"
elif "welshnewspapersonline" in f:
    tag = "WNO"
    hr = input('High resolution? [Y/N]')
    high_resolution = hr == 'Y' or hr == 'y'
else:
    tag = input('Site [BNA|WNO]: ')
    if tag != "BNA" and tag != "WNO":
        print("Site not supported. Exiting.")
        exit()
    if tag == "WNO":
        hr = input('High resolution? [Y/N]')
        high_resolution = hr == 'Y' or hr == 'y'

csv_path = "Crawler/Records/" + f + ".csv"
full_json_path = "Crawler/Records/" + f + ".json"

articles = []
with session_scope() as session:
    with open(csv_path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        print("Reading " + csv_path)
        try:
            firstrow = True
            for row in reader:
                if firstrow:
                    firstrow = False
                else:
                    try:
                        status = int(row[4])
                        if status is not None:
                            articles.append((row[0], row[1], row[2], status, row[5], row[6], row[7]))
                    except ValueError:
                        pass

        except csv.Error:
            print("File does not exists")

    if len(articles) > 0:
        print("Procesing articles")
        jarray = None
        if os.path.isfile(full_json_path):
            with open(full_json_path, 'rb') as jsonfile:
                info = jsonfile.read()
                info = info.strip()
                info = f"[{info[:-1]}]"
                jarray = json.loads(info)

        for article in articles:
            candidate_id = article[0]
            article_url = article[1]
            article_title = article[2]
            article_status = article[3]
            g_status = article[4]
            article_doc_title = article[5]
            status_writer = article[6]
            if g_status is None or g_status == "":
                g_status = article_status
            if status_writer is None:
                status_writer = 'gary'
            print("Processing ", article_doc_title, f"({article_title})")

            jarticle = None
            candidate_document = None
            publication_date = None
            county = ""
            if jarray is None:
                candidate_document = session.query(CandidateDocument)\
                    .filter(CandidateDocument.id == candidate_id).first()
                publication_date = candidate_document.publication_date
                county = candidate_document.publication_location
            else:
                if tag == "BNA":
                    jarticle = next((row for row in jarray if row['download_url'] == article_url), None)
                    publication_date = datetime.datetime.strptime(jarticle['publish'], "%A %d %B %Y")
                    county = jarticle['county']
                elif tag == "WNO":
                    jarticle = next((row for row in jarray if row['download_page'] == article_url), None)
                    publication_date = jarticle['publish'][:4].replace('st', '').replace('nd', '').replace('rd', '') \
                        .replace('th', '')
                    publication_date += jarticle['publish'][4:]
                    publication_date = datetime.datetime.strptime(publication_date, "%d%B%Y")

            if jarticle is not None or candidate_document is not None:
                publication_date = '{0.year:4d}-{0.month:02d}-{0.day:02d}'.format(publication_date)
                if article_status == 1:
                    file_processed = False
                    art_uploaded = False
                    description_article = None
                    download_page = None
                    ocr = None
                    type_ = None
                    newspaper = None
                    words = None
                    des = None

                    if len(article_doc_title) > 100:
                        article_doc_title = article_doc_title[:99]
                    doc_title = article_doc_title.decode('latin-1').encode('latin-1', 'ignore')

                    if len(article_title) > 100:
                        article_title = article_title[:99]
                    article_title = article_title.decode('latin-1').encode('latin-1', 'ignore')
                    if jarticle is not None:
                        description_article = jarticle['description']
                        ocr = jarticle['ocr'].encode('latin-1', 'ignore')
                        download_page = jarticle['download_page']
                        newspaper = jarticle['newspaper']
                        type_ = jarticle['type_']
                        words = jarticle['word']
                        des = description_article.encode('latin-1', 'ignore')
                    else:
                        description_article = candidate_document.description
                        download_page = candidate_document.url
                        newspaper = candidate_document.publication_title
                        type_ = candidate_document.type
                        words = candidate_document.word_count
                        des = description_article

                    check_if_exists = session.query(PortalDocument.id) \
                        .filter(PortalDocument.ocr == ocr) \
                        .filter(PortalDocument.url == download_page).all()
                    if len(check_if_exists) is 0:
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

                        if tag == "BNA":
                            try:
                                item_url = article_url.replace("download", "items")
                                handler = BNAHandler(item_url)
                                if document.ocr is None or document.ocr == '':
                                    ocr = get_ocr_bna(download_page, session=handler.s)
                                    document.ocr = ocr.encode('latin-1', 'ignore')
                                insert(session, document)
                                update_candidate(session, candidate_id, str(article_status), g_status, status_writer)
                                print("Candidate document status updated")
                                print("Downloading article")
                                handler.download_and_upload_file(document.id)
                                print("Article downloaded and uploaded to the server")
                                file_processed = True
                                art_uploaded = True
                            except Exception as e:
                                print(e)
                                print("Problem with article. Please use the update_pdf_files.py script.")
                        # elif tag == "WNO":
                        #     try:
                        #         handler = WNOHandler(article_url)
                        #         insert(session, document)
                        #         update_candidate(session, candidate_id, str(article_status), g_status, status_writer)
                        #         print "Candidate document status updated"
                        #         print "Downloading article"
                        #         if high_resolution:
                        #             handler.download_and_upload_high_resolution_image(document.id)
                        #             update_page_url(session, document.id,
                        #                             '/static/documents/' + str(document.id) + "/page.jpg")
                        #         else:
                        #             handler.download_and_upload_file(document.id)
                        #             update_page_url(session, document.id,
                        #                             '/static/documents/' + str(document.id) + "/page.jpg")
                        #         print "Article downloaded and uploaded to the server"
                        #         file_processed = True
                        #         dims = handler.get_dim()
                        #         art_tbs = handler.get_text_blocks()
                        #
                        #         if art_tbs is not None:
                        #             count = 0
                        #             arts_url = ""
                        #             for tb in art_tbs:
                        #                 print "Text Block #" + str(count + 1)
                        #                 if count != 0:
                        #                     arts_url += ";"
                        #                 x = round(float(tb['x']) * 100, 3)
                        #                 y = round(float(tb['y']) * 100, 3)
                        #                 w = round(float(tb['w']) * 100, 3)
                        #                 h = round(float(tb['h']) * 100, 3)
                        #
                        #                 y = y * float(dims[0]) / dims[1]
                        #                 h = h * float(dims[0]) / dims[1]
                        #                 cropped = handler.get_cropped_image(x, y, w, h)
                        #                 upload_file(document.id, cropped, "art" + str(count) + ".jpg")
                        #                 print "Cropped and uploaded"
                        #                 arts_url += "/static/documents/" + str(document.id) + "/art" + str(
                        #                     count) + ".pdf"
                        #                 count = count + 1
                        #             update_art_url(session, document.id, arts_url)
                        #             art_uploaded = True
                        #         else:
                        #             print "There was a problem obtaining the articles location"
                        #             if not high_resolution:
                        #                 print "Downloading high resolution image"
                        #                 handler.download_and_upload_high_resolution_image(document.id)
                        #                 update_page_url(session, document.id,
                        #                                 '/static/documents/' + str(document.id) + "/page.jpg")
                        #
                        #         print "Documents uploaded with success!"
                        #     except:
                        #         if not file_processed:
                        #             print "Problem with article. Please use the update_pdf_files.py script."

                        if file_processed:
                            update_page_url(session, document.id,
                                            '/static/documents/' + str(document.id) + "/page.pdf")
                            if art_uploaded:
                                update_art_url(session, document.id, '/static/documents/' +
                                               str(document.id) + "/art.pdf")
                            print("Portal document inserted")

                    else:
                        print(f"Article not inserted. An identical article is found at id = {check_if_exists[0].id}")
                        print("Updating status to 101")
                        update_candidate(session, candidate_id, '101', g_status, status_writer)
                else:
                    update_candidate(session, candidate_id, str(article_status), g_status, status_writer)
                    print("Candidate document status updated")
            else:
                print(f"Article not found in {full_json_path} or in database")

    else:
        print("nothing!")
