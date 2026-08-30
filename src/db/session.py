"""
Configuração da base de dados e de sessão
"""

from pathlib import Path
import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ..models.base import Base

# logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

# project-level database directory (project root)
project_root = Path(__file__).resolve().parents[2]
DB_DIR = project_root / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)
logger.info("Diretório para criação de tabelas disponível: %s", DB_DIR)

# database URL (file inside DB_DIR)
_db_file = DB_DIR / "tuneFinder.sqlite3"
db_url: str = f"sqlite:///{_db_file.as_posix()}"

# create engine
engine: Engine = create_engine(db_url, echo=False)

# Session factory
Session = sessionmaker(bind=engine)


def init_db(create: bool = True) -> None:
    """Criação de tabelas no banco de dados

    Arguments:
        create: se True, cria tabelas
    """
    if create:
        Base.metadata.create_all(engine)
        logger.info("Banco de dados inicializado em %s", db_url)