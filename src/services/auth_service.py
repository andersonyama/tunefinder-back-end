from __future__ import annotations

from ..models import User
from ..repositories.user_repository import create_user


class AuthValidationError(ValueError):
    """Base validation error for authentication operations."""


class UserAlreadyExistsError(AuthValidationError):
    """Raised when the username already exists."""


class InvalidCredentialsError(AuthValidationError):
    """Raised when the username or password is invalid."""


def _normalize_username(username: str | None) -> str:
    return (username or '').strip()


def register_user(username: str, password: str) -> User:
    normalized_username = _normalize_username(username)
    normalized_password = password or ''

    if not normalized_username or not normalized_password:
        raise AuthValidationError('Nome de usuário e senha são obrigatórios')

    if len(normalized_password) < 8:
        raise AuthValidationError('A senha deve ter pelo menos 8 caracteres')

    if User.query.filter_by(username=normalized_username).first():
        raise UserAlreadyExistsError('Nome de usuário já cadastrado')

    user = User(username=normalized_username, password=normalized_password)
    return create_user(user)


def authenticate_user(username: str, password: str) -> User:
    normalized_username = _normalize_username(username)
    user = User.query.filter_by(username=normalized_username).first()

    if not user or not user.verify_password(password or ''):
        raise InvalidCredentialsError('Nome de usuário ou senha inválidos')

    return user
