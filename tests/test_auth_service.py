import pytest

from src.db.session import db
from src.main import create_app
from src.models import User
from src.services.auth_service import (
    AuthValidationError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    authenticate_user,
    register_user,
)


@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app


def test_register_user_raises_for_missing_fields(app_context):
    with pytest.raises(AuthValidationError, match='obrigatórios'):
        register_user('', '12345678')


def test_register_user_raises_for_existing_username(app_context):
    register_user('alice', '12345678')

    with pytest.raises(UserAlreadyExistsError, match='já cadastrado'):
        register_user('alice', '87654321')


def test_authenticate_user_rejects_invalid_password(app_context):
    register_user('bob', '12345678')

    with pytest.raises(InvalidCredentialsError, match='inválidos'):
        authenticate_user('bob', 'wrong-password')

    user = authenticate_user('bob', '12345678')
    assert isinstance(user, User)
    assert user.username == 'bob'
