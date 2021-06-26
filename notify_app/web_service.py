from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import pytz

from notify_app import schemas, workers, config
from notify_app.mock import users
from notify_app.database import Base, engine, SessionLocal
from notify_app.crud import create_message


# Создать приложение FastAPI

app = FastAPI()


# Создать, настроить и запустить планировщик APScheduler

scheduler = BackgroundScheduler(**config.SCHEDULER_CONFIG)
scheduler.start()


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


# Создать и настроить логгер


# API endpoints

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
    print(f'Received task to send message at {type(message.send_date)}{message.send_date}')

    # Записать сообщение в базу данных

    create_message(db=db, message=message)  # ASYNC

    # Получить список пользователей для рассылки

    user_list = users.get_user_list()

    # Разослать сообщение пользователям
    # С УЧЁТОМ: 1. ДАТЫ НАЧАЛА РАССЫЛКИ 2. ТАЙМЗОНЫ ПОЛЬЗОВАТЕЛЯ

    # for user in user_list:
    #     if user.email:
    #         workers.send_by_email.send(address=user.email, message=message.text, subject=f'{message.subject} for {user.name}')

    for user in user_list:
        if not user.email:
            continue

        # scheduler.add_job(
        #     workers.send_by_email.send(address=user.email, message=message.text, subject=f'{message.subject} for {user.name}'),
        #     DateTrigger.from_crontab("* * * * *"),
        # )