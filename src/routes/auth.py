from flask import Blueprint, request, jsonify
from flask_openapi3 import APIBlueprint, Tag
from flask_login import login_user, logout_user, login_required, current_user

from ..schemas import *
from ..repositories import create_user
from ..models import User

auth_tag = Tag(name='Authentication', description='Authentication manegement endpoints')
auth_bp = APIBlueprint('auth', __name__, url_prefix='/auth', abp_tags=[auth_tag])

@auth_bp.post('/register', summary='Create an user')
def register(body: UserCreateRequest):
    username = body.username
    password = body.password

    if not username or not password:
        return jsonify({'error': 'Nome de usuário e senha são obrigatórios'}), 400

    if len(password) < 8:
        return jsonify({'error': 'A senha deve ter pelo menos 8 caracteres'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Nome de usuário já cadastrado'}), 409

    novo_usuario = User(username=username, password=password)
    create_user(novo_usuario)

    return jsonify({
        'mensagem': 'Usuário criado com sucesso', 
        'usuario': {'id': novo_usuario.id, 'username': novo_usuario.username}
    }), 201


@auth_bp.post('/login', summary='Login with an existing user')
def login(body: UserLoginRequest):
    username = body.username
    password = body.password

    usuario = User.query.filter_by(username=username).first()

    if not usuario or not usuario.verify_password(password):
        return jsonify({'error': 'Nome de usuário ou senha inválidos'}), 401

    login_user(usuario)  # cria a sessão e envia o cookie na resposta
    return jsonify({
        'mensagem': 'Login realizado com sucesso',
        'usuario': {'id': usuario.id, 'username': usuario.username}
    }), 200


@auth_bp.post('/logout', summary='Logout from the existing session')
@login_required
def logout():
    logout_user()
    return jsonify({'mensagem': 'Logout realizado com sucesso'}), 200