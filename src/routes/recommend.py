from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify

from ..clients.lastfm_client import lastfm_client
from ..lastfm.lastfm import LastFmApiError

from ..schemas import RecommendRequest
from ..services.recommend_service import suggest_artists

recommend_tag = Tag(name='Recommend', description='Artist recommendation endpoints')
recommend_bp = APIBlueprint("recommend", __name__, url_prefix="/recommend", abp_tags=[recommend_tag])

@recommend_bp.post("", summary="List of artists recommendation given a list of artists")
def recommend(body: RecommendRequest):
    try:
        data = suggest_artists(body.artist_ids)
    except LastFmApiError as e:
        return jsonify({"error": str(e)}), 502
    return jsonify(data)