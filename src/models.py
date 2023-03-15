from datetime import datetime

from sqlalchemy import Column, ForeignKey, \
    Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import declarative_base, relationship


# создаем базовый класс для определения моделей таблиц
Base = declarative_base()


# Таблица пользователей
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, nullable=False)

    # Связь с таблицей оригинальных изображений
    original_images = relationship('OriginalImage', back_populates='owner')

    def __repr__(self) -> str:
        return f'User#{self.id}: {self.username}'


# Таблица исходных изображений
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
        'RenderedImage', back_populates='original_image'
    )

    def __repr__(self) -> str:
        return f'OriginalImage#{self.id}: "{self.filename}" ' + \
            f'by User#{self.owner.id}'


# Таблица отрендеренных изображений
class RenderedImage(Base):
    __tablename__ = 'rendered_images'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    filename = Column(String, nullable=False)
    image = Column(LargeBinary, nullable=False)
    original_id = Column(Integer, ForeignKey('original_images.id'),
                         nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.now)

    # Связь с таблицей исходных изображений
    original_image = relationship(
        'OriginalImage', back_populates='rendered_images'
    )

    def __repr__(self) -> str:
        return f'RenderedImage#{self.id}: "{self.filename}" ' + \
            f'by OriginalImage#{self.original_image.id}'
