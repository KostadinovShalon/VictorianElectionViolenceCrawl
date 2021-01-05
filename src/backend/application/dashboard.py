from flask import Blueprint, jsonify

from repositories import candidates_repo, portal_documents_repo, searches_repo

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('')
def get_dashboard():
    total_searches = searches_repo.get_total_searches()
    total_candidates = candidates_repo.get_total_candidates()
    total_portal = portal_documents_repo.get_total_portal_documents()
    last_searches, _ = searches_repo.get_searches(5, 0, 'id', True)
    last_candidates, _ = candidates_repo.get_candidates(None, 5, 0, 'id', True)
    last_portal, _ = portal_documents_repo.get_portal_documents(5, 0, 'id', True)
    return jsonify({"searches_count": total_searches,
                    "candidates_count": total_candidates,
                    "portal_count": total_portal,
                    "last_searches": last_searches,
                    "last_candidates": last_candidates,
                    "last_portal": last_portal})


@bp.route('total_searches')
def get_total_searches():
    return str(searches_repo.get_total_searches())


@bp.route('total_candidates')
def get_total_candidates():
    return str(candidates_repo.get_total_candidates())


@bp.route('total_portal')
def get_total_portal():
    return str(portal_documents_repo.get_total_portal_documents())


@bp.route('last_searches')
def get_last_searches():
    last_searches, _ = searches_repo.get_searches(5, 0, 'id', True)
    return jsonify(last_searches)


@bp.route('last_candidates')
def get_last_candidates():
    last_candidates, _ = candidates_repo.get_candidates(None, 5, 0, 'id', True)
    return jsonify(last_candidates)


@bp.route('last_portal')
def get_last_portal():
    last_portal, _ = portal_documents_repo.get_portal_documents(5, 0, 'id', True)
    return jsonify(last_portal)
