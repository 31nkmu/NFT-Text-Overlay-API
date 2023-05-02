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


# Аутентификация
AUTH_JWT_STRATEGY_SECRET = os.getenv('AUTH_JWT_STRATEGY_SECRET')
AUTH_JWT_MANAGER_SECRET = os.getenv('AUTH_JWT_MANAGER_SECRET')


# Базы данных.
if DEBUG:
    db_name = 'elemint.db'
    db_engine_settings = f'sqlite:///{db_name}'
    async_db_engine_settings = f'sqlite+aiosqlite:///{db_name}'
else:
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    database = os.getenv('DATABASE')
    db_uri = f'{user}:{password}@{host}:{port}/{database}'
    db_engine_settings = f'postgresql://{db_uri}'
    async_db_engine_settings = f'postgresql+asyncpg://{db_uri}'


# Рассылка электронных писем
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_SENDER = os.getenv('SMTP_SENDER')
