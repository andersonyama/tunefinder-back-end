from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from ..schemas import *
from ..repositories import create_user
from ..models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    input_data = request.get_json()
    username = input_data.get('username')
    password = input_data.get('password')

    if not username or not password:
        return jsonify({'error': 'Nome de usuário e senha são obrigatórios'}), 400

    if len(password) < 8:
        return jsonify({'error': 'A senha deve ter pelo menos 8 caracteres'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Nome de usuário já cadastrado'}), 409

    novo_usuario = User(username=username, password=password)
    create_user(novo_usuario)

    return jsonify({'mensagem': 'Usuário criado com sucesso', 'id': novo_usuario.id}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    username = dados.get('username')
    password = dados.get('password')

    usuario = User.query.filter_by(username=username).first()

    if not usuario or not usuario.verify_password(password):
        return jsonify({'error': 'Nome de usuário ou senha inválidos'}), 401

    login_user(usuario)  # cria a sessão e envia o cookie na resposta
    return jsonify({
        'mensagem': 'Login realizado com sucesso',
        'usuario': {'id': usuario.id, 'username': usuario.username}
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'mensagem': 'Logout realizado com sucesso'}), 200


@auth_bp.route('/perfil', methods=['GET'])
@login_required
def perfil():
    """Rota protegida - exemplo de como consumir o usuário logado."""
    return jsonify({
        'id': current_user.id,
        'username': current_user.username
    }), 200