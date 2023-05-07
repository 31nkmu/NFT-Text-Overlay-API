from datetime import datetime

from sqlalchemy import Column, ForeignKey, \
    Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import relationship

from src.auth.database import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    # Связь с таблицей пользователей
    owner = relationship("User", back_populates="projects")

    # Связь с таблицей сертификатов
    certificates = relationship("Certificate", back_populates="project", cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'Project {self.id} by {self.owner.username}: {self.name}'


class Certificate(Base):
    __tablename__ = 'certificates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    image = Column(LargeBinary, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))

    # Связь с таблицей проектов
    project = relationship("Project", back_populates="certificates")

    def __repr__(self) -> str:
        return f'Certificate {self.id}: {self.filename}'


class TemplateImage(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'))


class PublicTemplate(TemplateImage):
    __tablename__ = 'public_templates'

    def __repr__(self) -> str:
        return f'Public template {self.id}: {self.name}'


class PrivateTemplate(TemplateImage):
    __tablename__ = 'private_templates'
    owner_id = Column(Integer, ForeignKey('users.id'))

    # Связь с таблицей пользователей
    owner = relationship("User", back_populates="templates")

    def __repr__(self) -> str:
        return f'Private Template {self.id}: {self.name}'
