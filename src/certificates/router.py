from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from src.auth.models import User
from src.certificates import database as db
from src.certificates import models, schemas, utils

certificates_router = APIRouter()


@certificates_router.post('/templates/upload', status_code=status.HTTP_201_CREATED)
def create_original_image(user_id: int, image: UploadFile = File(...),
                          db: Session = Depends(db.get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    original_image = models.PublicTemplate(
        filename=image.filename,
        image=image.file.read(),
        owner_id=user_id
    )
    db.add(original_image)
    db.commit()
    db.refresh(original_image)

    return {
        'id': original_image.id,
        'filename': original_image.filename,
        'owner_id': original_image.owner_id
    }


@certificates_router.post("/templates/package-render/",
                          status_code=status.HTTP_201_CREATED)
def render_package(table: schemas.Table, db: Session = Depends(db.get_db)):
    response = []
    for row in table.body:
        # Ищем оригинальное изображение в базе данных
        original_image = db.query(models.PublicTemplate) \
            .filter(models.PublicTemplate.id == row.template_id).first()
        if not original_image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Original image not found")

        # Рендерим изображение
        rendered_image_data, format = utils.render_image(
            original_image.image, row
        )

        # Сохраняем отрендеренное изображение в базе данных
        filename = utils.generate_filename(original_image, db)
        rendered_image = models.Certificate(
            filename=filename,
            image=rendered_image_data,
        )
        db.add(rendered_image)
        db.commit()
        db.refresh(rendered_image)

        # Кодируем изображение в строку base64
        encoded_image = utils.binary_to_base64(rendered_image_data, format)

        # Возвращаем информацию
        # об отрендеренном изображении и закодированную строку
        response.append({
            'id': rendered_image.id,
            'filename': rendered_image.filename,
            'image': encoded_image
        })

    return response


@certificates_router.get('/images/rendered/{image_id}')
def get_rendered_image(image_id: int, db: Session = Depends(db.get_db)):
    # Ищем отрендеренное изображение в базе данных
    rendered_image = db.query(models.Certificate)\
        .filter(models.Certificate.id == image_id).first()
    if not rendered_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Rendered image not found")

    image_stream, image_format = utils.create_an_image_buffer(rendered_image)

    # Возвращаем изображение как поток байтов
    # с заголовком "image/{image_format}"
    return StreamingResponse(image_stream, media_type=f"image/{image_format}")
