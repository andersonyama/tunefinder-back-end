from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify

from ..clients.lastfm_client import lastfm_client
from ..lastfm.lastfm import LastFmApiError

from ..schemas import ArtistSearchRequest

artist_tag = Tag(name='Artist', description='Artist operations')
artist_bp = APIBlueprint("artist", __name__, url_prefix="/artist", abp_tags=[artist_tag])

@artist_bp.get("/search", summary="Search for an artist")
def search(query: ArtistSearchRequest):
    try:
        data = lastfm_client.artist_search(query.artist)
    except LastFmApiError as e:
        return jsonify({"error": str(e)}), 502
    return jsonify(data)