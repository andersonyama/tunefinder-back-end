from datetime import datetime, UTC
from typing import Optional

from ..db.session import db

class FavoriteArtist(db.Model):
    __tablename__ = 'favorite_artists'

    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    id_artist = db.Column(db.String, primary_key=True)
    artist_name = db.Column(db.String)
    ts_added = db.Column(db.DateTime, nullable=False, default=datetime.now(UTC))
    note = db.Column(db.String)

    def __init__(self, id_user: int, id_artist: str, artist_name: str, note: Optional[str]):
        """
        Create a favorited artist

        Arguments:
            id_user: int
            id_artist: str
            artist_name: str
            note: str
        """
        self.id_user = id_user
        self.id_artist = id_artist
        self.artist_name = artist_name
        self.note = note