import os
from dotenv import load_dotenv

load_dotenv()
LASTFM_API_URL = os.getenv('LASTFM_API_URL')
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')