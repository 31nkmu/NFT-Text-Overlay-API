from fastapi import FastAPI, \
    Depends, File, \
    UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from . import database as db, models, schemas, utils


app = FastAPI()


# ПОЛЬЗОВАТЕЛИ

@app.get("/users")
def read_users(skip: int = 0, limit: int = 100,
               db: Session = Depends(db.get_db)):
    return db.query(models.User).offset(skip).limit(limit).all()


@app.post("/users/create", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate,
                db: Session = Depends(db.get_db)):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.put("/users/{user_id}")
def update_user(user_id: int, username: str = None,
                db: Session = Depends(db.get_db)):
    db_user = db.query(models.User)\
        .filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    if username:
        db_user.username = username
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(db.get_db)):
    db_user = db.query(models.User)\
        .filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": f"User {db_user.username} has been deleted"}


# ШАБЛОНЫ

@app.post('/templates/upload', status_code=status.HTTP_201_CREATED)
def create_original_image(user_id: int, image: UploadFile = File(...),
                          db: Session = Depends(db.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    original_image = models.OriginalImage(
        filename=image.filename,
        image=image.file.read(),
        user_id=user_id
    )
    db.add(original_image)
    db.commit()
    db.refresh(original_image)

    return {
        'id': original_image.id,
        'filename': original_image.filename,
        'owner_id': original_image.user_id
    }


@app.post("/templates/package-render", status_code=status.HTTP_201_CREATED)
def render_package(table: schemas.Table, db: Session = Depends(db.get_db)):
    response = []
    for row in table.body:
        # Ищем оригинальное изображение в базе данных
        original_image = db.query(models.OriginalImage)\
            .filter(models.OriginalImage.id == row.template_id).first()
        if not original_image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Original image not found")

        # Рендерим изображение
        rendered_image_data, format = utils.render_image(
            original_image.image, row
        )

        # Сохраняем отрендеренное изображение в базе данных
        filename = utils.generate_filename(original_image, db)
        rendered_image = models.RenderedImage(
            filename=filename,
            image=rendered_image_data,
            original_id=original_image.id,
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
            'original_image_id': rendered_image.original_id,
            'image': encoded_image
        })

    return response


@app.get('/images/rendered/{image_id}')
def get_rendered_image(image_id: int, db: Session = Depends(db.get_db)):
    # Ищем отрендеренное изображение в базе данных
    rendered_image = db.query(models.RenderedImage)\
        .filter(models.RenderedImage.id == image_id).first()
    if not rendered_image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Rendered image not found")

    image_stream, image_format = utils.create_an_image_buffer(rendered_image)

    # Возвращаем изображение как поток байтов
    # с заголовком "image/{image_format}"
    return StreamingResponse(image_stream, media_type=f"image/{image_format}")
