import crochet
from flask import Blueprint, request, jsonify, send_file
from sqlalchemy import func

from FilesHandler.download_candidates import CandidateDownloader
from FilesHandler.ocr_updater import update_ocr
from db.databasemodels import ArchiveSearchResult, CandidateDocument
from db.db_session import session_scope
from FilesHandler.BNAHandler import BNAHandler

import configuration

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
        return jsonify(get_candidates(ids, limit, page, sortBy, sortDesc))
    else:
        if current_activity_info["uploading"] and isinstance(candidate_downloader, CandidateDownloader):
            current_activity_info["total"] = len(candidate_downloader.articles_to_process)
            current_activity_info["index"] = candidate_downloader.processing_article_index
            current_activity_info["status"] = candidate_downloader.status[1]

        elif request.method == 'PUT':
            data = request.json
            start_candidates_processing(data)
            return jsonify(current_activity_info)
    return jsonify(current_activity_info)


@bp.route('/preview', methods=("GET",))
def get_article_preview():
    candidate_id = request.args.get("id")
    handler = BNAHandler(candidate_id, configuration.get_login_details())
    handler.download_full_pages()
    handler.create_cropped_image()
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
        ocr = update_ocr(int(_id))
        return ocr if ocr is not None else ("", 404)
    else:
        return "", 404


@crochet.run_in_reactor
def start_candidates_processing(articles):
    global candidate_downloader
    global current_activity_info

    current_activity_info["uploading"] = True
    candidate_downloader = CandidateDownloader(articles)
    candidate_downloader.update_and_download_candidates()
    candidate_downloader.flush_files()
    current_activity_info["uploading"] = False


def get_candidates(ids, limit, page, sort_by, desc):
    cands = []
    with session_scope() as session:
        needing_coding = session.query(CandidateDocument) \
            .filter(CandidateDocument.status != '0') \
            .filter(CandidateDocument.status != "1")
        if ids is not None:
            results = session.query(ArchiveSearchResult.url) \
                .filter(ArchiveSearchResult.archive_search_id.in_(ids))
            needing_coding = needing_coding.filter(CandidateDocument.url.in_(results))
        # fieldnames = ['id', 'url', 'publication_title', 'description', 'status',
        #               'g_status', 'title', 'status_writer']
        if sort_by is not None and sort_by in ["id", "title", "publication_title", "publication_location", "status",
                                               "publication_date", "description"]:
            if sort_by == "id":
                needing_coding = needing_coding.order_by(CandidateDocument.id.desc()) if desc \
                    else needing_coding.order_by(CandidateDocument.id)
            if sort_by == "description":
                needing_coding = needing_coding.order_by(CandidateDocument.description.desc()) if desc \
                    else needing_coding.order_by(CandidateDocument.description)
            elif sort_by == "title":
                needing_coding = needing_coding.order_by(CandidateDocument.title.desc()) if desc \
                    else needing_coding.order_by(CandidateDocument.title)
            elif sort_by == "publication_title":
                needing_coding = needing_coding.order_by(CandidateDocument.publication_title.desc()) if desc \
                    else needing_coding.order_by(CandidateDocument.publication_title)
            elif sort_by == "publication_location":
                needing_coding = needing_coding.order_by(CandidateDocument.publication_location.desc()) if desc \
                    else needing_coding.order_by(CandidateDocument.publication_location)
            elif sort_by == "status":
                needing_coding = needing_coding.order_by(CandidateDocument.status.desc()) if desc \
                    else needing_coding.order_by(CandidateDocument.status)
            else:
                needing_coding = needing_coding.order_by(CandidateDocument.publication_date.desc()) if desc \
                    else needing_coding.order_by(CandidateDocument.publication_date)
        else:
            needing_coding = needing_coding.order_by(CandidateDocument.id.desc())
        needing_coding = needing_coding.limit(limit).offset(limit * page)
        cands += [r.to_dict() for r in needing_coding.all()]
    return {"candidates": cands, "total": get_count_candidates(ids)}


def get_count_candidates(ids):
    with session_scope() as session:
        results = session.query(func.count(CandidateDocument.id)) \
            .filter(CandidateDocument.status != '0') \
            .filter(CandidateDocument.status != "1")
        if ids is not None:
            search_urls = session.query(ArchiveSearchResult.url) \
                .filter(ArchiveSearchResult.archive_search_id.in_(ids))
            results = results.filter(CandidateDocument.url.in_(search_urls))
    return results.first()[0]
