from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from notify_app import schemas, workers
from notify_app.mock import users
from notify_app.database import Base, engine, SessionLocal
from notify_app.crud import create_message

app = FastAPI()


# Создать базу данных и структуру таблиц (без миграций)

Base.metadata.create_all(bind=engine)


def get_db():
    """
    Возвращает новую сессию подключения к БД.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/send_message/')
def start_dramatiq_action(message: schemas.MessageSchema, db: Session = Depends(get_db)):
    """
    URI, предоставляющий функционал для рассылки сообщения.

    :param db:
    :param message: Сообщение в формате
        {
            'subject': <subject: Optional[str]=''>,
            'text': <text: str>,
            'send_date': <send_date: Optional[datetime]>
        }
    :return:
    """

    # Записать сообщение в базу данных

    create_message(db=db, message=message)  # ASYNC

    # Получить список пользователей для рассылки

    user_list = users.get_user_list()

    # Разослать сообщение пользователям
    # С УЧЁТОМ: 1. ДАТЫ НАЧАЛА РАССЫЛКИ 2. ТАЙМЗОНЫ ПОЛЬЗОВАТЕЛЯ

    for user in user_list:
        if user.email:
            workers.send_by_email.send(address=user.email, message=message.text, subject=message.subject)
