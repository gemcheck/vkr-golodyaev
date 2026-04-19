import sys
import logging
import os
from dotenv import load_dotenv

BASE_DIR = '/mnt/c/vkr-golodyaev/tests/web'
sys.path.insert(0, BASE_DIR)

# Явно загружаем .env из папки проекта
load_dotenv(os.path.join(BASE_DIR, '.env'))

from app import app as application
