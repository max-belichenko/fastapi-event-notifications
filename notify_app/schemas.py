from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class Message(BaseModel):
    id: int
    subject: Optional[str] = ''
    text: str
