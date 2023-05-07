from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from src.auth.database import Base
from src.certificates.models import Project, PrivateTemplate


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, nullable=False)
    organization = Column(String)
    email = Column(String(320), unique=True, index=True, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    hashed_password = Column(String(1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Связь с таблицей проектов
    projects = relationship(Project, back_populates="owner", cascade='all, delete-orphan')

    # Связь с таблицей приватных шаблонов
    templates = relationship(PrivateTemplate, back_populates="owner", cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'User {self.id}: {self.username}'
