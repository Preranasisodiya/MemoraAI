from datetime import datetime

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    title: str
    filename: str
    file_type: str
    file_path: str


class DocumentResponse(BaseModel):
    id: int
    user_id: int
    title: str
    filename: str
    file_type: str
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True