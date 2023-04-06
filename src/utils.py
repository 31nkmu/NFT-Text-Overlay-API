import json
import base64
from pathlib import Path
from io import BytesIO
from typing import Any

from PIL import Image, ImageDraw, ImageFont
from sqlalchemy.orm import Session

from . import config, models, schemas


def render_image(image: bytes, params: schemas.InsertTextParams):  # noqa: C901
    # Открываем изображение и создаем объект ImageDraw
    image = Image.open(BytesIO(image))
    draw = ImageDraw.Draw(image)

    for _, field_data in params.fields.items():
        # Вычисляем размер поля и шрифт для текста
        text = field_data.text
        coordinates = field_data.coordinates
        font = field_data.font

        font_path = font.path
        font_color = font.color
        font_optimal_size = font.optimal_size
        font_min_size = font.min_size

        # Получаем координаты для текста
        x0, y0 = coordinates[0]  # верхний левый угол
        x1, y1 = coordinates[2]  # нижний правый угол
        field_width = x1 - x0
        field_height = y1 - y0

        # Уменьшаем шрифт и переносим текст на новую строку при необходимости
        font_size = font_optimal_size
        font = ImageFont.truetype(font_path, font_size)
        while True:
            text_width, text_height = draw.textsize(text, font)
            if text_width <= field_width and text_height <= field_height:
                break
            font_size -= 1
            if font_size < font_min_size:
                font_size = font_min_size
                break
            font = ImageFont.truetype(font_path, font_size)

        # Разбиваем текст на несколько подстрок, если необходимо
        lines = []
        line = ''
        for word in text.split():
            test_line = line + word + ' '
            test_line_width, _ = draw.textsize(test_line, font)
            if test_line_width > field_width:
                lines.append(line.strip())
                line = word + ' '
            else:
                line = test_line
        if line:
            lines.append(line.strip())

        # Вычисляем позицию текста в каждой строке
        text_y = y0 + (field_height - len(lines) * text_height) // 2
        for line in lines:
            text_width, _ = draw.textsize(line, font)
            text_x = x0 + (field_width - text_width) // 2
            draw.text((text_x, text_y), line, font=font, fill=font_color)
            text_y += text_height

    # Конвертируем изображение обратно в бинарный формат и возвращаем
    img_bytes = BytesIO()
    image.save(img_bytes, format=image.format)

    return img_bytes.getvalue(), image.format


def create_an_image_buffer(rendered_image: models.RenderedImage):
    # Вытягиваем формат изображения
    with Image.open(BytesIO(rendered_image.image)) as img:
        image_format = img.format.lower()

    # Создаем байтовый поток и сохраняем изображение в него
    image_stream = BytesIO(rendered_image.image)

    return image_stream, image_format


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


def read_file(file_path: Path, mode: str = 'r',
              encoding: str = 'utf-8') -> Any:
    with open(file_path, mode, encoding) as content:
        return content.read()


def get_abi_data(abi_filepath: Path =
                 config.BASE_DIR.joinpath('abi.json')) -> Any:
    return json.loads(read_file(abi_filepath))
