import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv('./.env')

USER_ID = os.environ.get('USER_ID')
PASS_WORD = os.environ.get('PASS_WORD')
URL_PATH = os.environ.get('URL_PATH')
DB_UNIX_SOCKET = os.environ.get('DB_UNIX_SOCKET')
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASS_WORD = os.environ.get('DB_PASS_WORD')
DB_NAME = os.environ.get('DB_NAME')
PHANTOMJS_PATH = os.environ.get('PHANTOMJS_PATH')