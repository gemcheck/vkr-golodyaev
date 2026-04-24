import sys
import logging
import os
from dotenv import load_dotenv

# не забыть поменять путь
BASE_DIR = '/var/www/vkr-golodyaev/tests/web'
sys.path.insert(0, BASE_DIR)


load_dotenv(os.path.join(BASE_DIR, '.env'))

from app import app as application
