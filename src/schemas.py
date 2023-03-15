from pydantic import BaseModel, Field
from typing import List


class UserCreate(BaseModel):
    username: str


class UserOut(BaseModel):
    id: int
    username: str


class TextArea(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    text: str
    font: str
    font_size: int = Field(ge=0)
    color: str


class TemplateData(BaseModel):
    template: int = Field(ge=0)
    text_areas: List[TextArea]
