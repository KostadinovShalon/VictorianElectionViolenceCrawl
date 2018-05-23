import csv
import json
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
                    if status == 1 or status == 2 or status == 0:
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
                update_candidate(candidate_id, str(article_status))
                print "Candidate document updated"
                if article_status == 1:
                    document = PortalDocument(source_id=tag, doc_title=article_doc_title.encode('latin-1', 'ignore'),
                                              pdf_location="", pdf_page_location="",
                                              ocr=jarticle['ocr'].encode('latin-1', 'ignore'),
                                              pdf_thumbnail_location="No", candidate_document_id=candidate_id,
                                              description=jarticle['description'].encode('latin-1', 'ignore'),
                                              publication_date=publication_date,
                                              publication_location=county.encode('latin-1', 'ignore'),
                                              publication_title=jarticle['newspaper'].encode('latin-1', 'ignore'),
                                              title=jarticle['title'].encode('latin-1', 'ignore'),
                                              type=jarticle['type_'].encode('latin-1', 'ignore'),
                                              url=jarticle['download_page'], word_count=jarticle['word'])
                    insert(document)
                    print "Portal document inserted"
                    if tag == "BNA":
                        item_url = article_url.replace("download", "items")
                        handler = BNAHandler(item_url)
                        print "Downloading article"
                        article_file = handler.download_and_upload_file(document.id)
                        print "Article downloaded and uploaded to the server"
                        update_page_url(document.id, 'static/documents/' + str(document.id) + "/page.pdf")
                        update_art_url(document.id, 'static/documents/' + str(document.id) + "/art.pdf")
                        print "Documents updated with success!"
                    elif tag == "WNO":
                        handler = WNOHandler(article_url)
                        print "Downloading article"
                        if high_resolution:
                            handler.download_and_upload_high_resolution_image(document.id)
                            update_page_url(document.id, 'static/' + str(document.id) + "/page_HR.jpg")
                        else:
                            handler.download_and_upload_file(document.id)
                            update_page_url(document.id, 'static/' + str(document.id) + "/page.jpg")
                        print "Article downloaded and uploaded to the server"

                        dims = handler.get_dim()
                        art_tbs = handler.get_text_blocks()

                        if art_tbs is not None:
                            count = 0
                            arts_url = ""
                            for tb in art_tbs:
                                print "Text Block #" + str(count + 1)
                                if count != 0:
                                    arts_url += ";"
                                x = round(float(tb['x'])*100, 3)
                                y = round(float(tb['y']) * 100, 3)
                                w = round(float(tb['w']) * 100, 3)
                                h = round(float(tb['h']) * 100, 3)

                                y = y * float(dims[0]) / dims[1]
                                h = h * float(dims[0]) / dims[1]
                                cropped = handler.get_cropped_image(x, y, w, h)
                                upload_file(document.id, cropped, "art" + str(count) + ".jpg")
                                print "Cropped and uploaded"
                                arts_url += "static/" + str(document.id) + "/art" + str(count) + ".pdf"
                                count = count + 1
                            update_art_url(document.id, arts_url)
                        else:
                            print "There was a problem obtaining the articles location"
                            if not high_resolution:
                                print "Downloading high resolution image"
                                handler.download_and_upload_high_resolution_image(document.id)
                                update_page_url(document.id, 'static/' + str(document.id) + "/page_HR.jpg")

                        print "Documents uploaded with success!"

            else:
                print "Article not found in " + full_json_path


else:
    print "nothing!"
