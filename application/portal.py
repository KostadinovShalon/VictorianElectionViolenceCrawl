import crochet
from flask import Blueprint, request, jsonify
from sqlalchemy import func

from FilesHandler.portal_document_updater import PortalDocumentsUpdater
from db.databasemodels import PortalDocument
from db.db_session import session_scope

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
    return jsonify(get_portal_documents(limit, page, sortBy, sortDesc))


@bp.route('update', methods=('GET', 'PUT',))
def update_files():
    global current_activity_info
    global document_uploader

    if current_activity_info["updating"]:
        current_activity_info["status"] = document_uploader.status[1]
    elif request.method == 'PUT':
        _id = request.data
        if _id:
            start_updating(int(_id))
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


@crochet.run_in_reactor
def start_updating(document_id):
    global document_uploader
    global current_activity_info

    current_activity_info["updating"] = True
    document_uploader = PortalDocumentsUpdater(document_id)
    document_uploader.update_documents()
    document_uploader.flush_files()
    current_activity_info["updating"] = False


def get_portal_documents(limit, page, sort_by, desc):
    docs = []
    with session_scope() as session:
        docs_query = session.query(PortalDocument)
        if sort_by is not None and sort_by in ["id", "title", "publication_title", "publication_location",
                                               "publication_date", "type", "word_count", "description"]:
            if sort_by == "id":
                docs_query = docs_query.order_by(PortalDocument.id.desc()) if desc \
                    else docs_query.order_by(PortalDocument.id)
            if sort_by == "description":
                docs_query = docs_query.order_by(PortalDocument.description.desc()) if desc \
                    else docs_query.order_by(PortalDocument.description)
            elif sort_by == "title":
                docs_query = docs_query.order_by(PortalDocument.doc_title.desc()) if desc \
                    else docs_query.order_by(PortalDocument.doc_title)
            elif sort_by == "publication_title":
                docs_query = docs_query.order_by(PortalDocument.publication_title.desc()) if desc \
                    else docs_query.order_by(PortalDocument.publication_title)
            elif sort_by == "publication_location":
                docs_query = docs_query.order_by(PortalDocument.publication_location.desc()) if desc \
                    else docs_query.order_by(PortalDocument.publication_location)
            elif sort_by == "type":
                docs_query = docs_query.order_by(PortalDocument.type.desc()) if desc \
                    else docs_query.order_by(PortalDocument.type)
            elif sort_by == "word_count":
                docs_query = docs_query.order_by(PortalDocument.word_count.desc()) if desc \
                    else docs_query.order_by(PortalDocument.word_count)
            else:
                docs_query = docs_query.order_by(PortalDocument.publication_date.desc()) if desc \
                    else docs_query.order_by(PortalDocument.publication_date)
        else:
            docs_query = docs_query.order_by(PortalDocument.id.desc())
        total = session.query(func.count(PortalDocument.id)).first()[0]
        docs_query = docs_query.limit(limit).offset(limit * page)
        docs += [r.to_dict() for r in docs_query.all()]
        for doc in docs:
            if doc["pdf_uri"] is not None and doc["pdf_uri"] != "":
                doc["pdf_uri"] = "https://coders.victorianelectionviolence.uk" + doc["pdf_uri"]
            if doc["cropped_pdf_uri"] is not None and doc["cropped_pdf_uri"] != "":
                doc["cropped_pdf_uri"] = "https://coders.victorianelectionviolence.uk" + doc["cropped_pdf_uri"]
    return {"documents": docs, "total": total}
