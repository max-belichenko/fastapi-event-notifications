import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    name: str                                   # Ф.И.О.
    phone: Optional[str] = None                 # Номер телефона
    email: Optional[EmailStr] = None            # E-mail
    timezone: Optional[str] = 'Europe/Moscow'   # Таймзона по умолчанию +3:00 UTC (Москва)


class UserDB(User):
    id: int


class Message(BaseModel):
    subject: Optional[str] = ''             # Тема сообщения
    text: str                               # Текст сообщения
    send_date: Optional[datetime] = None    # Дата и время отправки (не ранее)


class MessageDB(Message):
    id: int
    time_created: datetime.datetime         # Дата и время создания записи в БД


