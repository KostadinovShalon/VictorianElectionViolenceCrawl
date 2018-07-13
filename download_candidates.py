import csv
import json
from DB import dbconn
from DB.dbconn import update_candidate, insert, update_art_url, update_page_url
from FilesHandler.BNAHandler import BNAHandler
from FilesHandler.WNOHandler import WNOHandler
from FilesHandler.FileHandler import upload_file
from DB.databasemodels import PortalDocument
import datetime

f = raw_input('JSON File (without extension): ')

high_resolution = False
if "britishnewspaperarchive" in f:
    tag = "BNA"
elif "welshnewspapersonline" in f:
    tag = "WNO"
    hr = raw_input('High resolution? [Y/N]')
    high_resolution = hr == 'Y' or hr == 'y'
else:
    tag = raw_input('Site [BNA|WNO]: ')
    if tag != "BNA" and tag != "WNO":
        print "Site not supported. Exiting."
        exit()
    if tag == "WNO":
        hr = raw_input('High resolution? [Y/N]')
        high_resolution = hr == 'Y' or hr == 'y'


full_name = "Crawler/Records/pending_" + f + ".csv"
full_json_path = "Crawler/Records/" + f + ".json"

articles = []

with open(full_name, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    print "Reading " + full_name
    try:
        firstrow = True
        for row in reader:
            if firstrow:
                firstrow = False
            else:
                try:
                    status = int(row[4])
                    if status is not None:
                        articles.append((row[0], row[1], row[2], status, row[5]))
                except ValueError:
                    pass

    except csv.Error:
        print "File does not exists"

if len(articles) > 0:
    print "Procesing articles"
    with open(full_json_path, 'rb') as jsonfile:
        info = jsonfile.read()
        info = info.strip()
        info = "[" + info[:-1] + "]"
        jarray = json.loads(info)
        for article in articles:
            candidate_id = article[0]
            article_url = article[1]
            article_title = article[2]
            article_status = article[3]
            article_doc_title = article[4]
            print "Processing " + article_doc_title + "(" + article_title + ")"

            jarticle = None
            publication_date = None
            county = ""
            if tag == "BNA":
                jarticle = next((row for row in jarray if row['download_url'] == article_url), None)
                publication_date = datetime.datetime.strptime(jarticle['publish'], "%A%d%B%Y")
                county = jarticle['county']
            elif tag == "WNO":
                jarticle = next((row for row in jarray if row['download_page'] == article_url), None)
                publication_date = jarticle['publish'][:4].replace('st', '').replace('nd', '').replace('rd', '')\
                    .replace('th', '')
                publication_date += jarticle['publish'][4:]
                publication_date = datetime.datetime.strptime(publication_date, "%d%B%Y")
            if jarticle is not None:
                publication_date = '{0.year:4d}-{0.month:02d}-{0.day:02d}'.format(publication_date)
                #update_candidate(candidate_id, str(article_status))
                if article_status == 1:
                    file_processed = False
                    art_uploaded = False
                    description_article = jarticle['description']
                    jtitle = jarticle['title']
                    if len(article_doc_title) > 100:
                        article_doc_title = article_doc_title[:99]
                    if len(jtitle) > 100:
                        jtitle = jtitle[:99]
                    doc_title = article_doc_title.decode('latin-1').encode('latin-1', 'ignore')
                    des = description_article.encode('latin-1', 'ignore')
                    ocr = jarticle['ocr'].encode('latin-1', 'ignore')
                    check_if_exists = dbconn.session.query(PortalDocument.id)\
                                        .filter(PortalDocument.ocr == ocr)\
                                        .filter(PortalDocument.url == jarticle['download_page']).all()
                    if len(check_if_exists) is 0:
                        document = PortalDocument(source_id="2", doc_title=doc_title,
                                                  pdf_location="", pdf_page_location="",
                                                  ocr=ocr,
                                                  pdf_thumbnail_location="No", candidate_document_id=candidate_id,
                                                  description= des,
                                                  publication_date=publication_date,
                                                  publication_location=county,
                                                  publication_title=jarticle['newspaper'],
                                                  title=jtitle.encode('latin-1', 'ignore'),
                                                  type=jarticle['type_'],
                                                  url=jarticle['download_page'], word_count=jarticle['word'])

                        if tag == "BNA":
                            try:
                                item_url = article_url.replace("download", "items")
                                handler = BNAHandler(item_url)
                                print "Downloading article"
                                insert(document)
                                handler.download_and_upload_file(document.id)
                                print "Article downloaded and uploaded to the server"
                                file_processed = True
                                art_uploaded = True
                            except:
                                print "Problem with article. Please use the update_pdf_files.py script."
                        elif tag == "WNO":
                            try:
                                handler = WNOHandler(article_url)
                                insert(document)
                                print "Downloading article"
                                if high_resolution:
                                    handler.download_and_upload_high_resolution_image(document.id)
                                    update_page_url(document.id, '/static/documents/' + str(document.id) + "/page.jpg")
                                else:
                                    handler.download_and_upload_file(document.id)
                                    update_page_url(document.id, '/static/documents/' + str(document.id) + "/page.jpg")
                                print "Article downloaded and uploaded to the server"
                                file_processed = True
                                dims = handler.get_dim()
                                art_tbs = handler.get_text_blocks()

                                if art_tbs is not None:
                                    count = 0
                                    arts_url = ""
                                    for tb in art_tbs:
                                        print "Text Block #" + str(count + 1)
                                        if count != 0:
                                            arts_url += ";"
                                        x = round(float(tb['x']) * 100, 3)
                                        y = round(float(tb['y']) * 100, 3)
                                        w = round(float(tb['w']) * 100, 3)
                                        h = round(float(tb['h']) * 100, 3)

                                        y = y * float(dims[0]) / dims[1]
                                        h = h * float(dims[0]) / dims[1]
                                        cropped = handler.get_cropped_image(x, y, w, h)
                                        upload_file(document.id, cropped, "art" + str(count) + ".jpg")
                                        print "Cropped and uploaded"
                                        arts_url += "/static/documents/" + str(document.id) + "/art" + str(count) + ".pdf"
                                        count = count + 1
                                    update_art_url(document.id, arts_url)
                                    art_uploaded = True
                                else:
                                    print "There was a problem obtaining the articles location"
                                    if not high_resolution:
                                        print "Downloading high resolution image"
                                        handler.download_and_upload_high_resolution_image(document.id)
                                        update_page_url(document.id,
                                                        '/static/documents/' + str(document.id) + "/page.jpg")

                                print "Documents uploaded with success!"
                            except:
                                if not file_processed:
                                    print "Problem with article. Please use the update_pdf_files.py script."

                        if file_processed:
                            update_page_url(document.id,
                                            '/static/documents/' + str(document.id) + "/page.pdf")
                            if art_uploaded:
                                update_art_url(document.id, '/static/documents/' + str(document.id) + "/art.pdf")
                            print "Portal document inserted"

                    else:
                        print "Article not inserted. An identical article is found at id = " + str(check_if_exists[0].id)
                        print "Updating status to 101"
                        update_candidate(candidate_id, '101')
                else:
                    update_candidate(candidate_id, str(article_status))
                    print "Candidate document status updated"
            else:
                print "Article not found in " + full_json_path


else:
    print "nothing!"
