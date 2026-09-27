from flask_login import current_user, login_required
from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify

from ..schemas import (
    FavoriteArtistCreateRequest,
    FavoriteArtistDeleteRequest,
    FavoriteArtistEditRequest,
    favorite_artist_to_response,
    favorite_artists_to_list_response,
)
from ..services.favorite_artist_service import (
    FavoriteArtistAlreadyExistsError,
    FavoriteArtistNotFoundError,
    FavoriteArtistValidationError,
    add_favorite_artist,
    edit_favorite_artist,
    list_favorite_artists,
    remove_favorite_artist,
)

favorite_artist_tag = Tag(name='Favorite Artist', description='Favorite artist management endpoints')
favorite_artist_bp = APIBlueprint("favorite_artist", __name__, url_prefix="/favoriteArtist", abp_tags=[favorite_artist_tag])


@favorite_artist_bp.post("", summary="Add an artist to user's favorite list")
@login_required
def add_favorite(body: FavoriteArtistCreateRequest):
    try:
        favorite_artist = add_favorite_artist(
            current_user.id,
            body.id_artist,
            body.artist_name,
            body.note,
        )
        return jsonify(favorite_artist_to_response(favorite_artist)), 201
    except FavoriteArtistAlreadyExistsError as exc:
        return jsonify({"error": str(exc)}), 409
    except FavoriteArtistValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@favorite_artist_bp.get("", summary="List user's favorite artists")
@login_required
def list_favorites():
    try:
        favorite_artists = list_favorite_artists(current_user.id)
        return jsonify(favorite_artists_to_list_response(favorite_artists))
    except FavoriteArtistValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@favorite_artist_bp.put("", summary="Edit user's favorite artist")
@login_required
def edit_favorites(body: FavoriteArtistEditRequest):
    try:
        favorite_artist = edit_favorite_artist(current_user.id, body.id_artist, body.note)
        return jsonify({"message": "Favorite artist edited successfully", "favorite_artist": favorite_artist_to_response(favorite_artist)}), 200
    except FavoriteArtistNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
    except FavoriteArtistValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@favorite_artist_bp.delete("", summary="Remove an artist from user's favorite list")
@login_required
def remove_favorite(body: FavoriteArtistDeleteRequest):
    try:
        remove_favorite_artist(current_user.id, body.id_artist)
        return jsonify({"message": "Favorite artist removed successfully"}), 200
    except FavoriteArtistNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
    except FavoriteArtistValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500