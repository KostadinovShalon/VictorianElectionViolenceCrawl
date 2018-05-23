from io import BytesIO
from FileHandler import upload_file
import requests
from PIL import Image


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

    def get_dim(self):
        return int(self.searched_item['PageAreas'][0]['Width']), int(self.searched_item['PageAreas'][0]['Height'])

    def download_and_upload_file(self, document_id):
        # https://www.britishnewspaperarchive.co.uk/viewer/bl/0000289/19000102/021/0002
        full_resolution_url = self.j['Items'][0]['Images'][0]['UriPageOriginal']
        f = self.s.get(full_resolution_url)
        tmp = BytesIO(f.content)
        tmp.seek(0)

        im = Image.open(tmp)

        tmppdf = BytesIO()
        im.save(tmppdf, 'PDF', resolution=100.0)
        tmppdf.seek(0)
        upload_file(document_id, tmppdf, "page.pdf")
        self.crop_images(im, document_id)

    def crop_images(self, article_file, document_id):
        count = 0
        tmp = BytesIO()

        images = []
        widths = []
        heights = []
        # cropped = Image.new('RGB', self.get_dim())
        for page_area in self.searched_item['PageAreas']:
            print "Cropping #" + str(count + 1)
            xb = int(page_area['XBottomLeft']) * article_file.size[0] / self.get_dim()[0]
            yb = int(page_area['YBottomLeft']) * article_file.size[1] / self.get_dim()[1]
            xt = int(page_area['XTopRight']) * article_file.size[0] / self.get_dim()[0]
            yt = int(page_area['YTopRight']) * article_file.size[1] / self.get_dim()[1]
            im = article_file.crop((xb, yb, xt, yt))
            images.append(im)
            widths.append(im.size[0])
            heights.append(im.size[1])
            count = count + 1
        W = max(widths)
        cropped = Image.new('RGB', (W, sum(heights)))
        last_height = 0
        for i in range(len(images)):
            x = (W - images[i].size[0]) / 2
            cropped.paste(images[i], (x, last_height))
            last_height += images[i].size[1]
        cropped.save(tmp, 'PDF', resolution=100.0)
        tmp.seek(0)
        upload_file(document_id, tmp, "art.pdf")
        print "Cropped and uploaded"
