"""
Configuração da base de dados e de sessão
"""

from pathlib import Path
import logging

from flask_sqlalchemy import SQLAlchemy

# logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

# project-level database directory (project root)
project_root = Path(__file__).resolve().parents[2]
DB_DIR = project_root / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)
logger.info("Directory for table creation is available: %s", DB_DIR)

# database URL (file inside DB_DIR)
_db_file = DB_DIR / "tuneFinder.sqlite3"
db_url: str = f"sqlite:///{_db_file.as_posix()}"

# Flask-SQLAlchemy instance
db = SQLAlchemy()

def init_db(app=None, create: bool = True) -> None:
    """Criação de tabelas no banco de dados

    Arguments:
        app: instância da aplicação Flask
        create: se True, cria tabelas
    """
    if app is not None:        
        db.init_app(app)

    if create:
        if app is None:
            raise RuntimeError("An app instance is required before creating database tables.")
        with app.app_context():
            db.create_all()
        logger.info("Banco de dados inicializado em %s", db_url)