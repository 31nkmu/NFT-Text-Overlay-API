from fastapi_users import schemas
from pydantic import BaseModel


class UserDataMixin(BaseModel):
    username: str
    organization: str


class UserRead(UserDataMixin, schemas.BaseUser[int]):
    pass


class UserCreate(UserDataMixin, schemas.BaseUserCreate):
    pass


class UserUpdate(UserDataMixin, schemas.BaseUserUpdate):
    pass
