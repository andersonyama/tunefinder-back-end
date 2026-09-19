from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from flask_login import LoginManager
from flask import jsonify

from .config import API_URL, API_KEY, SECRET_KEY
from .db.session import db, init_db, db_url

from .models import User, FavoriteArtist

info = Info(title="TuneFinder API", version='1.0.0')
app = OpenAPI(__name__, info=info)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, supports_credentials=True)

# initialize SQLAlchemy with the app
init_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error': 'Não autenticado'}), 401

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# importa rotas após criação do app para que ele possa ser importado por routes
from .api import routes, auth_bp, user_tag
app.register_blueprint(auth_bp, url_prefix='/auth', tags=[user_tag])
