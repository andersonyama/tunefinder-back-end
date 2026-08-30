from ..models import User, FavoriteArtist
from ..db.session import Session

def insert_favorite_artist(favorite_artist: FavoriteArtist) -> FavoriteArtist:
    try:
        with Session() as session:
            session.add(favorite_artist)
            session.commit()
            session.refresh(favorite_artist)
        return favorite_artist
    except Exception as e:
        raise e
    
def delete_favorite_artist(favorite_artist: FavoriteArtist):
    try:
        with Session() as session:
            session.delete(favorite_artist)
            session.commit()            
    except Exception as e:
        raise e