from datetime import datetime, UTC

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from ..db.session import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    ts_created = db.Column(db.DateTime, nullable=False, default=datetime.now(UTC))

    favorite_artists = db.relationship(
        'FavoriteArtist',
        backref='user',
        lazy='select',
        cascade='all, delete-orphan'
    )

    def __init__(self, username: str, password: str):
        """
        Create an user

        Arguments:
            username: str
            password: str
        """
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.ts_created = datetime.now(UTC)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'