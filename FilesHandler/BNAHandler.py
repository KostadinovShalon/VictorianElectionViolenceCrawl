from io import BytesIO
from FileHandler import upload_file
import requests
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader


class BNAHandler:

    LOGIN_PAGE = "https://www.britishnewspaperarchive.co.uk/account/login"

    payload = {
        'Username': "nick.vivyan@durham.ac.uk",
        "Password": "EV19@Nick",
        "RememberMe": "false",
        "NextPage": ""}

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.britishnewspaperarchive.co.uk",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
        "Origin": "https://www.britishnewspaperarchive.co.uk",
        "Link": "<https://www.britishnewspaperarchive.co.uk/account/login>; rel=\"canonical\"",
        "X-Frame-Options": "SAMEORIGIN"
        }

    def __init__(self, item_url):
        self.s = requests.Session()
        self.s.post(self.LOGIN_PAGE, data=self.payload, headers=self.headers)
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

    ## Returns False if file could not be cropped
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

    def join_pdfs(self, pages):
        output = BytesIO()
        pdf_writer = PdfFileWriter()
        for page in pages:
            pdf_reader = PdfFileReader(page)
            pdf_writer.addPage(pdf_reader.getPage(0))
        pdf_writer.write(output)
        output.seek(0)
        return output

    def paste_images(self, images):
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