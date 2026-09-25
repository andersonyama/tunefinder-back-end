from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from flask_login import login_required, login_user, logout_user

from ..schemas.user_schema import UserCreateRequest, UserLoginRequest
from ..services.auth_service import (
    AuthValidationError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    authenticate_user,
    register_user,
)

auth_tag = Tag(name='Authentication', description='Authentication manegement endpoints')
auth_bp = APIBlueprint('auth', __name__, url_prefix='/auth', abp_tags=[auth_tag])


@auth_bp.post('/register', summary='Create an user')
def register(body: UserCreateRequest):
    try:
        user = register_user(body.username, body.password)
    except UserAlreadyExistsError as exc:
        return jsonify({'error': str(exc)}), 409
    except AuthValidationError as exc:
        return jsonify({'error': str(exc)}), 400

    return jsonify({
        'mensagem': 'Usuário criado com sucesso',
        'usuario': {'id': user.id, 'username': user.username}
    }), 201


@auth_bp.post('/login', summary='Login with an existing user')
def login(body: UserLoginRequest):
    try:
        user = authenticate_user(body.username, body.password)
    except InvalidCredentialsError as exc:
        return jsonify({'error': str(exc)}), 401

    login_user(user)
    return jsonify({
        'mensagem': 'Login realizado com sucesso',
        'usuario': {'id': user.id, 'username': user.username}
    }), 200


@auth_bp.post('/logout', summary='Logout from the existing session')
@login_required
def logout():
    logout_user()
    return jsonify({'mensagem': 'Logout realizado com sucesso'}), 200