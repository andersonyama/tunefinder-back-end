from datetime import datetime
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from .base import Base
from .favorite_artist import FavoriteArtist

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)
    ts_created: Mapped[datetime] = mapped_column(nullable=False)

    favorite_artists: Mapped[List["FavoriteArtist"]] = relationship(lazy='select', cascade='all, delete-orphan')

    def __init__(self, username: str):
        """
        Create an user

        Arguments:
            username: str
        """
        self.username = username
        self.ts_created = datetime.now()