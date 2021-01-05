import crochet
from flask import Blueprint, request, jsonify, send_file

from FilesHandler.download_candidates import CandidateDownloader
from FilesHandler.ocr_updater import update_ocr
from FilesHandler.BNAHandler import BNAHandler

from repositories import configuration
from repositories.candidates_repo import get_candidates

bp = Blueprint('candidates', __name__, url_prefix='/candidates')

current_activity_info = {
    "total": 0,  # Number of articles to process with status different than 1
    "index": -1,  # Index of article being processed
    "status": None,  # Worker status
    "uploading": False
}

candidate_downloader = None


@bp.route('', methods=("GET", "POST", "PUT"))
def candidates():
    global candidate_downloader
    global current_activity_info

    if request.method == 'POST':
        ids = request.json
        limit = int(request.args.get("limit")) if request.args.get("limit") is not None else 10
        page = int(request.args.get("page")) - 1 if request.args.get("page") is not None else 0
        sortBy = request.args.get("sortby")
        sortDesc = int(request.args.get("desc")) if request.args.get("desc") is not None else 0
        cands, total = get_candidates(ids, limit, page, sortBy, sortDesc, configuration.db_variables())
        return jsonify({"candidates": cands, "total": total})
    else:
        if current_activity_info["uploading"] and isinstance(candidate_downloader, CandidateDownloader):
            current_activity_info["total"] = len(candidate_downloader.articles_to_process)
            current_activity_info["index"] = candidate_downloader.processing_article_index
            current_activity_info["status"] = candidate_downloader.status[1]

        elif request.method == 'PUT':
            data = request.json
            start_candidates_processing(data, configuration.get_login_details(),
                                        configuration.server_variables(),
                                        configuration.db_variables())
            return jsonify(current_activity_info)
    return jsonify(current_activity_info)


@bp.route('/preview', methods=("GET",))
def get_article_preview():
    candidate_id = request.args.get("id")
    handler = BNAHandler(candidate_id, configuration.get_login_details(),
                         configuration.server_variables(),
                         configuration.db_variables())
    handler.download_full_pages()
    handler.create_cropped_image()
    db_vars = configuration.db_variables()
    if db_vars["local"]:
        return send_file(handler.temp_cropped_file_pdf_name)
    else:
        return send_file("../" + handler.temp_cropped_file_pdf_name)


@bp.route('/stop', methods=("DELETE",))
def stop_process():
    global candidate_downloader
    global current_activity_info

    if candidate_downloader is not None:
        candidate_downloader.cancel()

        current_activity_info["uploading"] = False
    return jsonify(current_activity_info)


@bp.route('/update-ocr', methods=("PUT",))
def update_candidate_ocr():
    _id = request.data
    if _id:
        ocr = update_ocr(int(_id), configuration.get_login_details(), configuration.db_variables())
        return ocr if ocr is not None else ("fail", 404)
    else:
        return "fail", 404


@crochet.run_in_reactor
def start_candidates_processing(articles, login_details, server_details, db_vars):
    global candidate_downloader
    global current_activity_info

    current_activity_info["uploading"] = True
    candidate_downloader = CandidateDownloader(articles, login_details, server_details, db_vars)
    candidate_downloader.update_and_download_candidates()
    candidate_downloader.flush_files()
    current_activity_info["uploading"] = False

