import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserSchema(BaseModel):
    name: str                                   # Ф.И.О.
    phone: Optional[str] = None                 # Номер телефона
    email: Optional[EmailStr] = None            # E-mail
    timezone: Optional[str] = 'Europe/Moscow'   # Таймзона по умолчанию +3:00 UTC (Москва)


class UserDBSchema(UserSchema):
    id: int


class MessageSchema(BaseModel):
    subject: Optional[str] = ''             # Тема сообщения
    text: str                               # Текст сообщения
    send_date: Optional[datetime] = None    # Дата и время отправки (не ранее)


class MessageDBSchema(MessageSchema):
    id: int
    time_created: datetime.datetime         # Дата и время создания записи в БД


