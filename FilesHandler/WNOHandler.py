from io import BytesIO
from FileHandler import upload_file
import requests
from PIL import Image


class WNOHandler:

    BASE_INFO_JSON_URL = "http://newspapers.library.wales/iiif/2.0/image/"
    BASE_ARTICLES_URL = "http://newspapers.library.wales/json/viewarticledata/llgc-id:"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/64.0.3282.167 Safari/537.36"
    }

    def __init__(self, article_url):
        self.s = requests.Session()
        params = article_url.split('/')
        self.artid = params[-2]
        self.pageid = params[-3]
        self.info_json_url = self.BASE_INFO_JSON_URL + str(self.pageid) + "/info.json"
        self.dim_article_url = self.BASE_ARTICLES_URL + str(self.pageid)

    def get_dim(self):
        resp = self.s.get(self.info_json_url, headers=self.headers)
        j = resp.json()
        return j["width"], j["height"]

    def get_text_blocks(self):
        try:
            resp = self.s.get(self.dim_article_url, timeout=8)
            j = resp.json()
            art_tbs = next((art['textBlocks'] for art in j if art['id'] == "ART" + str(self.artid)), None)
            return art_tbs
        except:
            return None

    def download_and_upload_file(self, document_id):
        download_url = self.BASE_INFO_JSON_URL + str(self.pageid) + "/full/512,/0/default.jpg"
        f = self.s.get(download_url)
        tmp = BytesIO(f.content)
        tmp.seek(0)
        upload_file(document_id, tmp, "page.jpg")
        return tmp

    def download_and_upload_high_resolution_image(self, document_id):
        dims = self.get_dim()
        nw = dims[0] / 512
        nh = dims[1] / 512
        n = nw * nh
        if nw * 512 < dims[0]:
            n += nh
        if nh * 512 < dims[1]:
            n += nw
        if nw * 512 < dims[0] and nh * 512 < dims[1]:
            n += 1

        im = Image.new('RGB', dims)
        count = 0
        for i in range(nh):
            h_im = Image.new('RGB', (dims[0], 512))
            for j in range(nw):
                count = count + 1
                print "Downloading " + str(count) + "/" + str(n)
                b_im = self.get_cropped_image(j*512, i*512)
                n_h_im = Image.open(b_im)
                h_im.paste(n_h_im, (j*512, 0))
            if nw * 512 < dims[0]:
                count = count + 1
                print "Downloading " + str(count) + "/" + str(n)
                b_im = self.get_cropped_image(nw * 512, i * 512, w=(dims[0] - nw*512))
                n_h_im = Image.open(b_im)
                h_im.paste(n_h_im, (nw * 512, 0))
            im.paste(h_im, (0, i*512))
            if nh * 512 < dims[1]:
                h_im = Image.new('RGB', (dims[0], (dims[1] - nh * 512)))
                for j in range(nw):
                    count = count + 1
                    print "Downloading " + str(count) + "/" + str(n)
                    b_im = self.get_cropped_image(j * 512, nh * 512, h=(dims[1] - nh * 512))
                    n_h_im = Image.open(b_im)
                    h_im.paste(n_h_im, (j * 512, 0))
                if nw * 512 < dims[0]:
                    count = count + 1
                    print "Downloading " + str(count) + "/" + str(n)
                    b_im = self.get_cropped_image(nw * 512, i * 512, w=(dims[0] - nw * 512), h=(dims[1] - nh * 512))
                    n_h_im = Image.open(b_im)
                    h_im.paste(n_h_im, (nw * 512, 0))
            im.paste(h_im, (0, nh * 512))
        imb = BytesIO()
        im.save(imb, 'jpeg')
        imb.seek(0)
        im.save('test10.jpg')
        print "Uploading image to the server. It may take several minutes"
        upload_file(document_id, imb, "page.jpg")

    def get_cropped_image(self, x, y, w=512, h=512):
        download_url = self.BASE_INFO_JSON_URL + str(self.pageid) \
                       + "/" + str(x) + "," + str(y) + "," \
                       + str(w) + "," + str(h) + ",/" + str(w) + "," + str(h) + ",/0/default.jpg"
        f = self.s.get(download_url)
        tmp = BytesIO(f.content)
        tmp.seek(0)
        return tmp
