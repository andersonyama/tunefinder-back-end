from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base

class FavoriteArtist(Base):
    __tablename__ = 'favorite_artists'

    id_user: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    id_artist: Mapped[str] = mapped_column(primary_key=True)
    ts_added: Mapped[datetime] = mapped_column(nullable=False)

    def __init__(self, id_user: int,id_artist: str):
            """
            Create a favorited artist
    
            Arguments:
                id_user: int
                id_artist: int
            """
            self.id_user = id_user
            self.id_artist = id_artist
            self.ts_added = datetime.now()