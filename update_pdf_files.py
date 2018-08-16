import sys
import os

from Crawler.utils.dbutils import session_scope

sys.path.append(os.path.abspath('..'))
from Crawler.utils.dbconn import update_page_url, update_art_url, update_candidate
from FilesHandler.BNAHandler import BNAHandler
from FilesHandler.WNOHandler import WNOHandler
from Crawler.utils.databasemodels import PortalDocument, CandidateDocument
import csv
import requests
from Crawler.utils import bna_login_utils as login
import sys, traceback

nargs = len(sys.argv)
slow = False
if nargs > 1:
    arg = str(sys.argv[1])
    if arg == 'slow':
        slow = True

payload = {
        'Username': login.username,
        "Password": login.password,
        "RememberMe": login.remember_me,
        "NextPage": login.next_page}
with session_scope() as session:

    result = session.query(PortalDocument.id, PortalDocument.url). \
             filter(PortalDocument.pdf_location == '').all()

    with open('nopdfarticles.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['id', 'url'])
        for row in result:
            writer.writerow([str(row.id), row.url])

    raw_input('Press Enter to continue')
    with open('nopdfarticles.csv', 'rb') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)
        try:
            s = requests.Session()
            s.post(login.login_url, data=payload, headers=login.headers)
            for row in reader:
                id_ = int(row[0])
                print 'Processing ' + str(id_)
                try:
                    if 'www.britishnewspaperarchive.co.uk' in row[1]:
                        item_url = row[1].replace("download/", "")
                        item_url = item_url.replace("viewer", "viewer/items")
                        handler = BNAHandler(item_url, session=s, slow=slow)
                        print "Downloading article"
                        cropped = handler.download_and_upload_file(id_)
                        update_page_url(session, id_, '/static/documents/' + str(id_) + "/page.jpg")
                        if cropped:
                            update_art_url(session, id_, '/static/documents/' + str(id_) + "/art.jpg")
                        else:
                            update_art_url(session, id_, '/static/documents/' + str(id_) + "/page.jpg")
                        cd = session.query(CandidateDocument.id, CandidateDocument.g_status,
                                           CandidateDocument.status_writer)\
                            .filter(CandidateDocument.url == row[1]).first()
                        update_candidate(session, cd.id, 1, cd.g_status, cd.status_writer)
                        print "Article downloaded and uploaded to the server"
                    elif 'newspapers.library.wales' in row[1]:
                        handler = WNOHandler(row[1])
                        handler.download_and_upload_high_resolution_image(id_)
                        update_page_url(session, id_, '/static/documents/' + str(id_) + "/page.jpg")
                    print row[1]
                except Exception as e:
                    print 'Problem with article ' + str(id_) + ": " + str(e)
                    traceback.print_exc(file=sys.stdout)

        except csv.Error:
            print "File does not exists"
