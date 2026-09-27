import pytest

from src.db.session import db
from src.main import create_app
from src.models import FavoriteArtist
from src.services.favorite_artist_service import (
    FavoriteArtistAlreadyExistsError,
    FavoriteArtistValidationError,
    add_favorite_artist,
    edit_favorite_artist,
    list_favorite_artists,
    remove_favorite_artist,
)


@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app


def test_add_and_list_favorite_artist(app_context):
    artist = add_favorite_artist(1, 'mbid-1', 'Artist One', 'favorite')

    assert isinstance(artist, FavoriteArtist)
    assert artist.id_user == 1
    assert artist.id_artist == 'mbid-1'

    items = list_favorite_artists(1)
    assert any(item.id_artist == 'mbid-1' for item in items)


def test_edit_favorite_artist(app_context):
    add_favorite_artist(1, 'mbid-2', 'Artist Two', 'old note')

    updated = edit_favorite_artist(1, 'mbid-2', 'new note')
    assert updated.note == 'new note'


def test_remove_favorite_artist(app_context):
    add_favorite_artist(1, 'mbid-3', 'Artist Three', 'note')

    remove_favorite_artist(1, 'mbid-3')
    assert list_favorite_artists(1) == []


def test_add_favorite_artist_rejects_missing_required_fields(app_context):
    with pytest.raises(FavoriteArtistValidationError, match='obrigatórios'):
        add_favorite_artist(1, '', '', 'note')

    with pytest.raises(FavoriteArtistValidationError, match='obrigatórios'):
        add_favorite_artist(1, 'mbid-4', '', 'note')


def test_add_favorite_artist_rejects_duplicate(app_context):
    add_favorite_artist(1, 'mbid-5', 'Artist Five', 'note')

    with pytest.raises(FavoriteArtistAlreadyExistsError, match='já cadastrado'):
        add_favorite_artist(1, 'mbid-5', 'Artist Five', 'new note')
