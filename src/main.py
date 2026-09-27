from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from flask_login import LoginManager
from flask import jsonify, redirect

from .config import SECRET_KEY
from .db.session import init_db, db_url
from .models import User


def create_app() -> OpenAPI:
    info = Info(title="TuneFinder API", version='1.0.0')
    app = OpenAPI(__name__, info=info)

    app.config['SECRET_KEY'] = SECRET_KEY or 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True

    CORS(app, supports_credentials=True, origins=["http://localhost:8080"])

    init_db(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({'error': 'Não autenticado'}), 401

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    home_tag = Tag(name='Documentation', description='Tunefinder API documentation')

    @app.get('/', tags=[home_tag])
    def home():
        return redirect('/openapi/swagger')

    from .routes.auth import auth_bp
    from .routes.artist import artist_bp
    from .routes.recommend import recommend_bp
    from .routes.favorite_artist import favorite_artist_bp

    app.register_api(auth_bp)
    app.register_api(artist_bp)
    app.register_api(recommend_bp)
    app.register_api(favorite_artist_bp)

    return app


app = create_app()
