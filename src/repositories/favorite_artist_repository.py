from ..models import FavoriteArtist
from ..db.session import db

def insert_favorite_artist(favorite_artist: FavoriteArtist) -> FavoriteArtist:
    try:
        db.session.add(favorite_artist)
        db.session.commit()
        db.session.refresh(favorite_artist)
        return favorite_artist
    except Exception as e:
        raise e
    
def delete_favorite_artist(id_user: int, id_artist: str):
    try:
        favorite_artist = FavoriteArtist.query.filter_by(id_user=id_user, id_artist=id_artist).first()
        if favorite_artist is None:
            raise ValueError("Favorite artist not found")
        db.session.delete(favorite_artist)
        db.session.commit()
    except Exception as e:
        raise e

def list_favorite_artists(id_user: int):
    try:
        return FavoriteArtist.query.filter_by(id_user=id_user).all()
    except Exception as e:
        raise e

def edit_favorite_artist(id_user: int, id_artist: str, note: str):
    try:
        favorite_artist = FavoriteArtist.query.filter_by(id_user=id_user, id_artist=id_artist).first()
        if favorite_artist is None:
            raise ValueError("Favorite artist not found")
        favorite_artist.note = note
        db.session.commit()
    except Exception as e:
        raise e