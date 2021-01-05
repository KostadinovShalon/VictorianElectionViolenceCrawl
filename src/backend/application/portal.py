import crochet
from flask import Blueprint, request, jsonify, send_file
from repositories import configuration

from FilesHandler.portal_document_updater import PortalDocumentsUpdater
from repositories.portal_documents_repo import get_portal_documents, get_portal_document

bp = Blueprint('portal', __name__, url_prefix='/portal')

document_uploader = None
current_activity_info = {
    "status": None,
    "updating": False
}


@bp.route('')
def candidates():
    limit = int(request.args.get("limit")) if request.args.get("limit") is not None else 10
    page = int(request.args.get("page")) - 1 if request.args.get("page") is not None else 0
    sortBy = request.args.get("sortby")
    sortDesc = int(request.args.get("desc")) if request.args.get("desc") is not None else 0
    docs, total = get_portal_documents(limit, page, sortBy, sortDesc, configuration.db_variables())
    return jsonify({"documents": docs, "total": total})


@bp.route('update', methods=('GET', 'PUT',))
def update_files():
    global current_activity_info
    global document_uploader

    if current_activity_info["updating"]:
        current_activity_info["status"] = document_uploader.status[1]
    elif request.method == 'PUT':
        _id = request.data
        if _id:
            start_updating(int(_id), configuration.get_login_details(),
                           configuration.server_variables(),
                           configuration.db_variables())
            current_activity_info["updating"] = True
        else:
            return "", 404
    return jsonify(current_activity_info)


@bp.route('/update/stop', methods=("DELETE",))
def stop_process():
    global document_uploader
    global current_activity_info

    if document_uploader is not None:
        document_uploader.cancel()

        current_activity_info["updating"] = False
    return jsonify(current_activity_info)


@bp.route('/local/full')
def get_full_local_file():
    global document_uploader
    global current_activity_info

    _id = request.args.get("id")
    doc = get_portal_document(int(_id), configuration.db_variables())
    local_dir = doc.pdf_page_location
    return send_file(local_dir)


@bp.route('/local/cropped')
def get_cropped_local_file():
    global document_uploader
    global current_activity_info

    _id = request.args.get("id")
    doc = get_portal_document(int(_id), configuration.db_variables())
    local_dir = doc.pdf_location
    return send_file(local_dir)


@crochet.run_in_reactor
def start_updating(document_id, login_details, server_details, db_vars):
    global document_uploader
    global current_activity_info

    current_activity_info["updating"] = True
    document_uploader = PortalDocumentsUpdater(document_id, login_details, server_details, db_vars)
    document_uploader.update_documents()
    document_uploader.flush_files()
    current_activity_info["updating"] = False
