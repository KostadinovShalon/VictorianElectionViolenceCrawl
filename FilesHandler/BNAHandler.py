from io import BytesIO
from FileHandler import upload_file
import requests
from PIL import Image
import PyPDF2
from Crawler.utils import bna_login_utils as login


class BNAHandler:

    payload = {
        'Username': login.username,
        "Password": login.password,
        "RememberMe": login.remember_me,
        "NextPage": login.next_page}

    def __init__(self, item_url):
        self.s = requests.Session()
        self.s.post(login.login_url, data=self.payload, headers=login.headers)
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

    def get_dim(self):
        return int(self.searched_item['PageAreas'][0]['Width']), int(self.searched_item['PageAreas'][0]['Height'])

    def download_and_upload_file(self, document_id):
        # https://www.britishnewspaperarchive.co.uk/viewer/bl/0000289/19000102/021/0002ages'][0]['UriPageOriginal']
        pdfs = []
        images = []
        for page in self.original_pages:
            f = self.s.get(page)
            tmp = BytesIO(f.content)
            tmp.seek(0)
            im = Image.open(tmp)
            images.append({'identifier': page, 'image': im})
            tmppdf = BytesIO()
            im.save(tmppdf, 'PDF', resolution=100.0)
            tmppdf.seek(0)
            pdfs.append(tmppdf)

        page_pdf = self.join_pdfs(pdfs)

        upload_file(document_id, page_pdf, "page.pdf")
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
            page_images.append((art['identifier'], []))

        # cropped = Image.new('RGB', self.get_dim())
        for page_area in self.searched_item['PageAreas']:
            page_id = page_area['PageId']
            article_file = next((af for af in article_files if page_id in af['identifier']), None)
            if article_file is not None:
                print "Cropping #" + str(count + 1)
                xb = int(page_area['XBottomLeft']) * article_file['image'].size[0] / self.get_dim()[0]
                yb = int(page_area['YBottomLeft']) * article_file['image'].size[1] / self.get_dim()[1]
                xt = int(page_area['XTopRight']) * article_file['image'].size[0] / self.get_dim()[0]
                yt = int(page_area['YTopRight']) * article_file['image'].size[1] / self.get_dim()[1]
                im = article_file['image'].crop((xb, yb, xt, yt))
                for page_image in page_images:
                    if page_image[0] is article_file['identifier']:
                        page_image[1].append(im)
                        break
                count = count + 1

        for page_image in page_images:
            heights = [im.size[1] for im in page_image[1]]
            if sum(heights) > 65000:
                first = page_image[1][:len(page_image[1])/2]
                second = page_image[1][len(page_image[1])/2:]
                tmp1 = self.paste_images(first)
                tmp2 = self.paste_images(second)
                page_pdfs.append(tmp1)
                page_pdfs.append(tmp2)
            else:
                tmp = self.paste_images(page_image[1])
                page_pdfs.append(tmp)
        pdf = self.join_pdfs(page_pdfs)
        upload_file(document_id, pdf, "art.pdf")
        print "Cropped and saved"

    @staticmethod
    def join_pdfs(pages):
        output = BytesIO()
        pdf_writer = PyPDF2.PdfFileWriter()
        for page in pages:
            pdf_reader = PyPDF2.PdfFileReader(page)
            pdf_writer.addPage(pdf_reader.getPage(0))
        pdf_writer.write(output)
        output.seek(0)
        return output

    @staticmethod
    def paste_images(images):
        widths = [im.size[0] for im in images]
        heights = [im.size[1] for im in images]
        w = max(widths)
        cropped = Image.new('RGB', (w, sum(heights)))
        last_height = 0
        for i in range(len(images)):
            x = (w - widths[i]) / 2
            cropped.paste(images[i], (x, last_height))
            last_height += heights[i]
        tmp = BytesIO()
        cropped.save(tmp, 'PDF', resolution=100.0)
        tmp.seek(0)
        return tmp
