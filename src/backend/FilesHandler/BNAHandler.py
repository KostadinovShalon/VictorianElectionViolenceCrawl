import os
import shutil
from io import BytesIO
from repositories import configuration

import requests
from PIL import Image, ImageEnhance

from FilesHandler.FileHandler import upload_file
from repositories.candidates_repo import get_candidate_url_from_id


class BNAHandler:

    def __init__(self, candidate_id, login_details):
        self.login_details = login_details
        self.candidate_id = str(candidate_id)
        self.item_url = get_candidate_url_from_id(int(candidate_id))  # Per article data URL
        self.searched_item = None  # Dict containing information about the item. download_full_pages must be called
        self.downloaded_pages = {}  # PDf temporal file paths of article's pages. download_full_pages must be called
        self.temp_full_file_pdf_name = None
        self.temp_cropped_file_pdf_name = None
        self.local = configuration.server_variables()["local"]
        self.files_dir = configuration.server_variables()["files_dir"]
        if self.local:
            self.root_files_dir = os.path.join(self.files_dir, self.candidate_id)
        else:
            self.root_files_dir = os.path.join("temp", self.candidate_id)

    def download_full_pages(self, session=None):
        payload = {
            'Username': self.login_details["username"],
            "Password": self.login_details["password"],
            "RememberMe": self.login_details["remember_me"],
            "NextPage": self.login_details["next_page"]
        }
        self.downloaded_pages.clear()
        if not os.path.exists(self.root_files_dir):
            os.makedirs(self.root_files_dir)

        if session is None:
            session = requests.Session()
            session.post(self.login_details["login_url"], data=payload, headers=self.login_details["headers"])  # Login
        session.get(self.item_url.replace('download/', ''))  # Needed for getting access to the article
        resp = session.get(self.item_url.replace('download/', 'items/')).json()
        # This gives a dict with It, Title, Type, PageAreas, Images and PublicTags
        self.searched_item = next((item for item in resp['Items'] if item['Id'] == resp['CurrentItemId']), None)
        unique_fn = self.searched_item['Id'].replace('/', '_')
        self.temp_full_file_pdf_name = os.path.join(self.root_files_dir, f"page.pdf")

        if os.path.exists(self.temp_full_file_pdf_name):
            return

        # This gives a unique list with article images
        original_pages = list(dict.fromkeys(image['UriPageOriginal'] for image in self.searched_item['Images']))
        print(f"Pages: {len(original_pages)}")

        for page_count, page in enumerate(original_pages):
            print('Downloading page ', page_count, page)
            f = session.get(page, headers={'User-Agent': self.login_details['headers']["User-Agent"]})
            print('Page ', page_count, ' downloaded')
            tmp = BytesIO(f.content)
            tmp.seek(0)
            with Image.open(tmp) as im:
                temp_fn = os.path.join(self.root_files_dir, f"{unique_fn}_{page_count + 1}.png")
                im.save(temp_fn, 'PNG', resolution=100.0)
                self.downloaded_pages[page] = temp_fn
                print('Page ', page_count, ' temporally saved')
            tmp.close()
            f.close()
        join_pages(self.downloaded_pages.values(), self.temp_full_file_pdf_name)

    def flush(self):
        folder = os.path.join(self.root_files_dir)
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if self.local:  # Skipping final files if in local
                    if file_path in (self.temp_full_file_pdf_name, self.temp_cropped_file_pdf_name):
                        continue
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

    def upload_full_pages(self, document_id):
        if not self.local:
            if self.temp_full_file_pdf_name is None:
                raise Exception
            print('Uploading page pdf')
            upload_file(document_id, self.temp_full_file_pdf_name, "page.pdf")

    def create_cropped_image(self):
        page_images = []
        for (art_id, art_path) in self.downloaded_pages.items():
            page_images.append(
                {
                    "uri_id": art_id,
                    "filepath": art_path,
                    "cropped_filenames": [],
                    "coordinates": []
                })
        cropped_images = []
        cropped_pdfs = []
        self.temp_cropped_file_pdf_name = os.path.join(self.root_files_dir, "art.pdf")

        if os.path.exists(self.temp_cropped_file_pdf_name):
            return

        for count, page_area in enumerate(self.searched_item['PageAreas']):
            page_id = page_area['PageId']
            article_file = next((af for af in page_images if page_id in af['uri_id']), None)  #
            if article_file is not None:
                im = Image.open(article_file["filepath"])
                print(f"Cropping #{count + 1}")
                xb = int(page_area['XBottomLeft']) * im.size[0] / int(page_area['Width'])
                yb = int(page_area['YBottomLeft']) * im.size[1] / int(page_area['Height'])
                xt = int(page_area['XTopRight']) * im.size[0] / int(page_area['Width'])
                yt = int(page_area['YTopRight']) * im.size[1] / int(page_area['Height'])

                base_fp = article_file["filepath"].rsplit('.', 1)[0]
                cropped_filepath = f"{base_fp}_cropped_{count}.png"
                im.crop((xb, yb, xt, yt)).save(cropped_filepath, 'PNG', resolution=100.0)
                article_file["cropped_filenames"].append(cropped_filepath)
                cropped_images.append(cropped_filepath)
                article_file["coordinates"].append((xb, yb, xt, yt))

        for page_count, page_image in enumerate(page_images):
            tmp = paste_images(page_image["filepath"],
                               page_image["cropped_filenames"],
                               page_image["coordinates"],
                               page_count)
            cropped_pdfs.append(tmp)
        join_pages(cropped_pdfs, self.temp_cropped_file_pdf_name)
        for page in cropped_pdfs:
            os.remove(page)
        for page in cropped_images:
            os.remove(page)

    def upload_cropped_pages(self, document_id):
        if not self.local:
            if self.temp_cropped_file_pdf_name is None:
                raise Exception
            print('Uploading cropped pdf')
            upload_file(document_id, self.temp_cropped_file_pdf_name, "art.pdf")
            print("Cropped file uploaded")


def paste_images(base_page_filepath, images, coordinates, count):
    base_fp = base_page_filepath.rsplit('.', 1)[0]
    cropped = Image.open(base_page_filepath)
    enhancer = ImageEnhance.Brightness(cropped)
    cropped = enhancer.enhance(0.5)

    for i in range(len(images)):
        x = int(coordinates[i][0])
        y = int(coordinates[i][1])
        cropped.paste(Image.open(images[i]), (x, y))
    cropped_name = f"{base_fp}_temp_page_{count + 1}.png"
    cropped.save(cropped_name, 'png', resolution=100.0)
    cropped.close()
    return cropped_name


def join_pages(items, name):
    images = list(map(Image.open, items))
    if len(images) == 1:
        images[0].save(name, 'PDF', resolution=100.0)
    else:
        images[0].save(name, 'PDF', resolution=100.0, save_all=True, append_images=images[1:])
    for im in images:
        im.close()


if __name__ == '__main__':
    u = "https://www.britishnewspaperarchive.co.uk/viewer/items/bl/0000052/18000626/018/0003"

    handler = BNAHandler(1, configuration.get_login_details(prepend='../'))
    handler.download_full_pages()
    handler.create_cropped_image()
    handler.upload_full_pages(1)
    handler.upload_cropped_pages(1)
    handler.flush()
