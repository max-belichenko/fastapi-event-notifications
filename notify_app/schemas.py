from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class UserDB(User):
    id: int


class Message(BaseModel):
    subject: Optional[str] = ''
    text: str


class MessageDB(Message):
    id: int

