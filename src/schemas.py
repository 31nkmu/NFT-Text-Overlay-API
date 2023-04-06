from pydantic import BaseModel
from typing import List


class UserCreate(BaseModel):
    username: str


class UserOut(BaseModel):
    id: int
    username: str


class Font(BaseModel):
    path: str
    color: str
    optimal_size: int
    min_size: int


class Fields(BaseModel):
    text: str
    coordinates: List[List[int]]
    font: Font


class InsertTextParams(BaseModel):
    template_id: int
    fields: dict[str, Fields]


class Table(BaseModel):
    body: List[InsertTextParams]
