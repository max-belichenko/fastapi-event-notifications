from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

import logging

from notify_app import schemas, workers, config
from notify_app.crud import create_message
from notify_app.mock import users, html
from notify_app.database import Base, engine, SessionLocal
from notify_app.utils.sending_time import get_send_dt_for_user, add_timezone_if_empty
from notify_app.utils import websockets


# Создать и настроить логгер

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


# Создать приложение FastAPI

app = FastAPI()

# Создать менеджер управления соединениями WebSockets

websockets_manager = websockets.ConnectionManager()


# Создать, настроить и запустить планировщик APScheduler

scheduler = BackgroundScheduler(**config.SCHEDULER_CONFIG)
scheduler.start()


# Создать глобальный сериализуемый запускаемый объект для планировщика APScheduler

def send_by_email_callable(*args, **kwargs):
    workers.send_by_email.send(*args, **kwargs)


def send_by_websocket_callable(*args, **kwargs):
    workers.send_web_notification.send(*args, **kwargs)


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


# API endpoints

@app.post('/send_message/')
async def start_dramatiq_action(message: schemas.MessageSchema, db: Session = Depends(get_db)):
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

    await create_message(db=db, message=message)

    # Получить список пользователей для рассылки

    user_list = users.get_user_list()

    # Разослать сообщение пользователям из базы данных

    for user in user_list:

        # Отправить сообщение на E-mail

        if user.email:
            send_date = get_send_dt_for_user(
                send_date=add_timezone_if_empty(message.send_date, config.SERVER_TIMEZONE_STR),
                user_timezone=user.timezone,
                allowed_period=config.SEND_ALLOWED_PERIOD
            )

            scheduler.add_job(
                send_by_email_callable,
                'date',                     # Запустить выполнение в указанное время и дату
                run_date=send_date,
                args=(user.email, message.text, f'{message.subject} for {user.name}'),
                misfire_grace_time=None,    # Запустить выполнение, если время выполнения было пропущено (без ограничения срока давности)
            )

        # Отправить сообщение на телефон

        if user.phone:
            # Not implemented
            pass

    # Разослать сообщения пользователям через WebSockets
    send_date = message.send_date
    print('Scheduling websocket broadcast:')
    scheduler.add_job(
        send_by_websocket_callable,
        'date',                     # Запустить выполнение в указанное время и дату
        run_date=send_date,
        args=(websockets_manager, message.subject, message.text),
        misfire_grace_time=None,    # Запустить выполнение, если время выполнения было пропущено (без ограничения срока давности)
    )
    scheduler.print_jobs()

    # await websockets_manager.broadcast(f'"{message.subject}": "{message.text}"')


@app.get('/')
async def get():
    """
    Возвращает HTML-страницу для подключения через WebSocket.

    :return:
    """
    return HTMLResponse(html.index_html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Создаёт и обслуживает подключение по WebSocket.

    :param websocket:
    :return:
    """
    await websockets_manager.connect(websocket)
    while True:
        try:
            data = await websocket.receive()
            await websockets_manager.broadcast(f"Client #{websocket} says: {data}")
        except WebSocketDisconnect:
            websockets_manager.disconnect(websocket)
