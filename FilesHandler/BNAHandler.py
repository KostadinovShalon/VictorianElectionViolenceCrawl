from io import BytesIO
from FilesHandler.FileHandler import upload_file
import requests
from PIL import Image
import PyPDF2
from Crawler.utils import bna_login_utils as login
import os


class BNAHandler:
    payload = {
        'Username': login.username,
        "Password": login.password,
        "RememberMe": login.remember_me,
        "NextPage": login.next_page}

    def __init__(self, item_url, session=None, slow=False):
        self.slow = slow
        if session is None:
            self.s = requests.Session()
            self.s.post(login.login_url, data=self.payload, headers=login.headers)
        else:
            self.s = session
        self.s.get(item_url.replace('items/', ''))
        resp = self.s.get(item_url)
        self.j = resp.json()
        self.searched_item = next((item for item in self.j['Items'] if item['Id'] == '/'
                                  .join(item_url.split('/')[5:-1]).upper()), None)
        self.original_pages = []
        for image in self.searched_item['Images']:
            url = image['UriPageOriginal']
            if url not in self.original_pages:
                self.original_pages.append(url)
        resp.close()

    def get_dim(self):
        return int(self.searched_item['PageAreas'][0]['Width']), int(self.searched_item['PageAreas'][0]['Height'])

    def download_and_upload_file(self, document_id):
        # https://www.britishnewspaperarchive.co.uk/viewer/bl/0000289/19000102/021/0002ages'][0]['UriPageOriginal']
        pdfs = []
        images = []
        page_count = 1
        for page in self.original_pages:
            print('Downloading page ', page_count, page)
            f = self.s.get(page, headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) "
                                                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                        "Chrome/64.0.3282.167 Safari/537.36"})
            print('Page ', page_count, ' downloaded')
            tmp = BytesIO(f.content)
            tmp.seek(0)
            im = Image.open(tmp)
            images.append({'identifier': page, 'image': im})
            im.save("./temp" + str(page_count) + ".pdf", 'PDF', resolution=100.0)
            print('Page ', page_count, ' temporally saved')
            pdfs.append("temp" + str(page_count) + ".pdf")
            page_count = page_count + 1
            tmp.close()
            f.close()
        page_pdf = self.join_pdfs(pdfs, 'temp2upload.pdf')

        print('Uploading page pdf')
        upload_file(document_id, page_pdf, "page.pdf")
        os.remove('temp2upload.pdf')
        for page in pdfs:
            os.remove(page)
        if not (self.searched_item['PageAreas'][0]['Width'].isdigit()
                and self.searched_item['PageAreas'][0]['Height'].isdigit()):
            return False
        self.crop_images(images, document_id)
        return True

    def crop_images(self, article_files, document_id):
        count = 0

        page_images = []
        page_pdfs = []
        for art in article_files:
            page_images.append((art['identifier'], [], []))

        # cropped = Image.new('RGB', self.get_dim())
        for page_area in self.searched_item['PageAreas']:
            page_id = page_area['PageId']
            article_file = next((af for af in article_files if page_id in af['identifier']), None)
            if article_file is not None:
                print(f"Cropping #{count + 1}")
                xb = int(page_area['XBottomLeft']) * article_file['image'].size[0] / self.get_dim()[0]
                yb = int(page_area['YBottomLeft']) * article_file['image'].size[1] / self.get_dim()[1]
                xt = int(page_area['XTopRight']) * article_file['image'].size[0] / self.get_dim()[0]
                yt = int(page_area['YTopRight']) * article_file['image'].size[1] / self.get_dim()[1]

                for page_image in page_images:
                    if page_image[0] is article_file['identifier']:
                        if self.slow:
                            article_file['image'].crop((xb, yb, xt, yt)).save("cropped" + str(count) + ".png", 'PNG',
                                                                              resolution=100.0)
                            page_image[1].append("cropped" + str(count) + ".png")
                        else:
                            im = article_file['image'].crop((xb, yb, xt, yt))
                            page_image[1].append(im)
                        page_image[2].append((xb, yb, xt, yt))
                        break
                count = count + 1

        page_item_count = 1
        for page_image in page_images:
            min_x = 0
            min_y = 0
            max_x = 0
            max_y = 0
            for coordinates in page_image[2]:
                if min_x == 0 or coordinates[0] < min_x:
                    min_x = coordinates[0]
                if min_y == 0 or coordinates[1] < min_y:
                    min_y = coordinates[1]
                if coordinates[2] > max_x:
                    max_x = coordinates[2]
                if coordinates[3] > max_y:
                    max_y = coordinates[3]
            tmp = self.paste_images(page_image[1], page_image[2], (min_x, min_y, max_x, max_y), page_item_count)
            page_item_count = page_item_count + 1
            page_pdfs.append(tmp)
        pdf = self.join_pdfs(page_pdfs, 'temp2upload.pdf')
        upload_file(document_id, pdf, "art.pdf")
        os.remove('temp2upload.pdf')
        for page in page_pdfs:
            os.remove(page)
        if self.slow:
            for page_image in page_images:
                for page in page_image[1]:
                    os.remove(page)
        print("Cropped and saved")

    @staticmethod
    def join_pdfs(pages, name):
        merger = PyPDF2.PdfFileMerger()
        for page in pages:
            merger.append(page)
        with open(name, 'wb') as temp2upload:
            merger.write(temp2upload)
        merger.close()
        return name

    def paste_images(self, images, coordinates, limits, count):
        w = limits[2] - limits[0]
        h = limits[3] - limits[1]
        cropped = Image.new('RGB', (w, h))
        for i in range(len(images)):
            x = coordinates[i][0] - limits[0]
            y = coordinates[i][1] - limits[1]
            if self.slow:
                cropped.paste(Image.open(images[i]), (x, y))
            else:
                cropped.paste(images[i], (x, y))
        cropped.save("temp" + str(count) + ".pdf", 'PDF', resolution=100.0)
        cropped.close()
        return "temp" + str(count) + ".pdf"
