import base64
from io import BytesIO
from typing import List

from PIL import Image, ImageDraw, ImageFont
from sqlalchemy.orm import Session

from . import models, schemas


def render_image(image_data: bytes,
                 text_areas: List[schemas.TextArea]):
    # Загружаем изображение в Pillow
    with Image.open(BytesIO(image_data)) as img:
        draw = ImageDraw.Draw(img)

        # Добавляем текстовые поля
        for area in text_areas:
            font = ImageFont.truetype(area.font, size=area.font_size)
            draw.text(
                (area.x, area.y), area.text,
                fill=area.color, font=font
            )

        # Конвертируем изображение обратно в бинарный формат и возвращаем
        img_bytes = BytesIO()
        img.save(img_bytes, format=img.format)

        return img_bytes.getvalue(), img.format


def generate_filename(original: models.OriginalImage, db: Session) -> str:
    # Получаем оригинальное изображение из базы данных
    original = db.query(models.OriginalImage).get(original.id)
    if not original:
        raise ValueError(f"No original image found with id {original.id}")
    # Получаем владельца оригинального изображения из базы данных
    owner = db.query(models.User).get(original.owner.id)
    if not owner:
        raise ValueError(f"No user found with id {original.owner.id}")

    # Формируем базовое имя файла
    base_filename = original.filename.rsplit(".", 1)[0]
    suffix = 0
    # Ищем свободное имя файла с учетом суффикса
    while True:
        filename = f"{base_filename}" if suffix == 0 else \
            f"{base_filename} ({suffix})"
        # Если в базе данных нет изображения с таким именем, возвращаем это имя
        if not db.query(models.RenderedImage)\
                .filter_by(filename=filename).count():
            return filename
        # Иначе увеличиваем суффикс и повторяем поиск
        suffix += 1


def binary_to_base64(rendered_image_data: bytes, format: str) -> str:
    data = base64.b64encode(rendered_image_data).decode("utf-8").\
        replace('\n', '').replace('\r', '')  # Убираем лишние символы
    encoded_image = f'data:image/{format.lower()};base64,{data}'

    return encoded_image
