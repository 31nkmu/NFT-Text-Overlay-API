from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from .config import db_engine_settings  # ToDo: env

# создаем подключение к базе данных
engine = create_engine(db_engine_settings, echo=True)

# создаем таблицы в БД
Base.metadata.create_all(engine)

# создаем объект сессии базы данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


# функция для получения экземпляра сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
