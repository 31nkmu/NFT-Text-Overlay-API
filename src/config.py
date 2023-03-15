"""Server settings for project."""

import os
from pathlib import Path

from dotenv import load_dotenv


# Создавайте пути внутри проекта следующим образом: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))


# ПРЕДУПРЕЖДЕНИЕ ОБ БЕЗОПАСНОСТИ:
# не запускайте с включенной отладкой в продакшен среде!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'


# Базы данных.
if DEBUG:
    db_name = 'app.db'
    db_engine_settings = f'sqlite:///{db_name}'
else:
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    database = os.getenv('DATABASE')
    db_engine_settings = \
        f'postgresql://{user}:{password}@{host}:{port}/{database}'
