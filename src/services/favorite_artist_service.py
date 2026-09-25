from __future__ import annotations

from ..models import FavoriteArtist
from ..repositories.favorite_artist_repository import (
    delete_favorite_artist,
    edit_favorite_artist as update_favorite_artist,
    insert_favorite_artist,
    list_favorite_artists as get_favorite_artists,
)


class FavoriteArtistValidationError(ValueError):
    """Base validation error for favorite artist operations."""


class FavoriteArtistNotFoundError(FavoriteArtistValidationError):
    """Raised when a favorite artist cannot be found."""


class FavoriteArtistAlreadyExistsError(FavoriteArtistValidationError):
    """Raised when the artist is already saved for the same user."""


def _normalize(value: str | None) -> str:
    return (value or '').strip()


def add_favorite_artist(id_user: int, id_artist: str, artist_name: str, note: str | None = None) -> FavoriteArtist:
    normalized_id_user = int(id_user)
    normalized_id_artist = _normalize(id_artist)
    normalized_artist_name = _normalize(artist_name)

    if not normalized_id_user or not normalized_id_artist or not normalized_artist_name:
        raise FavoriteArtistValidationError('id_user, id_artist e artist_name são obrigatórios')

    existing_artist = FavoriteArtist.query.filter_by(
        id_user=normalized_id_user,
        id_artist=normalized_id_artist,
    ).first()
    if existing_artist:
        raise FavoriteArtistAlreadyExistsError('favorite_artist já cadastrado')

    favorite_artist = FavoriteArtist(
        normalized_id_user,
        normalized_id_artist,
        normalized_artist_name,
        note,
    )
    return insert_favorite_artist(favorite_artist)


def list_favorite_artists(id_user: int) -> list[FavoriteArtist]:
    normalized_id_user = int(id_user)
    if not normalized_id_user:
        raise FavoriteArtistValidationError('id_user é obrigatório')
    return get_favorite_artists(normalized_id_user)


def edit_favorite_artist(id_user: int, id_artist: str, note: str) -> FavoriteArtist:
    normalized_id_user = int(id_user)
    normalized_id_artist = _normalize(id_artist)
    normalized_note = note or ''

    if not normalized_id_user or not normalized_id_artist:
        raise FavoriteArtistValidationError('id_user e id_artist são obrigatórios')

    favorite_artist = FavoriteArtist.query.filter_by(
        id_user=normalized_id_user,
        id_artist=normalized_id_artist,
    ).first()
    if favorite_artist is None:
        raise FavoriteArtistNotFoundError('favorite_artist not found')

    favorite_artist.note = normalized_note
    update_favorite_artist(normalized_id_user, normalized_id_artist, normalized_note)
    return favorite_artist


def remove_favorite_artist(id_user: int, id_artist: str) -> None:
    normalized_id_user = int(id_user)
    normalized_id_artist = _normalize(id_artist)

    if not normalized_id_user or not normalized_id_artist:
        raise FavoriteArtistValidationError('id_user e id_artist são obrigatórios')

    favorite_artist = FavoriteArtist.query.filter_by(
        id_user=normalized_id_user,
        id_artist=normalized_id_artist,
    ).first()
    if favorite_artist is None:
        raise FavoriteArtistNotFoundError('favorite_artist not found')

    delete_favorite_artist(normalized_id_user, normalized_id_artist)
