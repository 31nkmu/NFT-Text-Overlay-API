from datetime import datetime

from sqlalchemy import Column, ForeignKey, \
    Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import relationship

from src.auth.database import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'))

    # Связь с таблицей пользователей
    owner = relationship("User", back_populates="projects")
    # Связь с таблицей сертификатов
    certificates = relationship("Certificate", back_populates="project")

    def __repr__(self) -> str:
        return f'Project {self.id} by {self.owner.username}: {self.name}'


class Certificate(Base):
    __tablename__ = 'certificates'

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    image = Column(LargeBinary, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    original_id = Column(Integer, ForeignKey('original_images.id'),
                         nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))

    # Связь с таблицей проектов
    project = relationship("Project", back_populates="certificates")

    def __repr__(self) -> str:
        return f'Certificate {self.id}: {self.filename}'


class TemplateImage:
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'))


class PublicTemplate(Base, TemplateImage):
    __tablename__ = 'public_templates'

    def __repr__(self) -> str:
        return f'Public template {self.id}: {self.name}'


class PrivateTemplate(Base, TemplateImage):
    __tablename__ = 'private_templates'

    # Связь с таблицей пользователей
    owner = relationship("User")

    def __repr__(self) -> str:
        return f'Private Template {self.id}: {self.name}'


class OriginalImage(Base):
    __tablename__ = 'original_images'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    filename = Column(String, nullable=False)
    image = Column(LargeBinary, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.now)

    # Связь с таблицей пользователей
    owner = relationship('User', back_populates='original_images')

    # Связь с таблицей отрендеренных изображений
    rendered_images = relationship(
        'Certificate', back_populates='original_image'
    )

    def __repr__(self) -> str:
        return f'OriginalImage#{self.id}: "{self.filename}" ' + \
            f'by User#{self.owner.id}'
