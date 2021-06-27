from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

import logging

from notify_app import schemas, workers, config
from notify_app.crud import create_message
from notify_app.mock import users, html
from notify_app import app_logger
from notify_app.database import Base, engine, SessionLocal
from notify_app.utils.sending_time import get_send_dt_for_user, add_timezone_if_empty
from notify_app.utils import websockets


# Создать и настроить логгер

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

logger = app_logger.get_logger(__name__)


# Создать приложение FastAPI

app = FastAPI()
logger.debug('Создано приложение FastAPI')

# Создать менеджер управления соединениями WebSockets

websockets_manager = websockets.ConnectionManager()
logger.debug('Создан WebSocket-менеджер')


# Создать, настроить и запустить планировщик APScheduler

scheduler = BackgroundScheduler(**config.SCHEDULER_CONFIG)
scheduler.start()
logger.debug(f'Запущен APScheduler ({config.SCHEDULER_CONFIG})')


# Создать глобальный сериализуемый запускаемый объект для планировщика APScheduler

def send_by_email_callable(*args, **kwargs):
    workers.send_by_email.send(*args, **kwargs)


# Создать базу данных и структуру таблиц (без миграций)

Base.metadata.create_all(bind=engine)
logger.debug(f'Создана база данных')


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
    logger.debug(f'POST:/send_message/')

    # Записать сообщение в базу данных

    logger.debug(f'Сохраняется сообщение в БД...')
    await create_message(db=db, message=message)
    logger.debug(f'ОК')

    # Получить список пользователей для рассылки

    user_list = users.get_user_list()

    # Разослать сообщение пользователям из базы данных

    for user in user_list:
        logger.debug(f'Отправляется сообщение пользователю {user}:')

        # Отправить сообщение на E-mail

        if user.email:
            send_date = get_send_dt_for_user(
                send_date=add_timezone_if_empty(message.send_date, config.SERVER_TIMEZONE_STR),
                user_timezone=user.timezone,
                allowed_period=config.SEND_ALLOWED_PERIOD
            )
            logger.debug(f'Время отправки: {send_date}')

            scheduler.add_job(
                send_by_email_callable,
                'date',                     # Запустить выполнение в указанное время и дату
                run_date=send_date,
                args=(user.email, message.text, f'{message.subject} for {user.name}'),
                misfire_grace_time=None,    # Запустить выполнение, если время выполнения было пропущено (без ограничения срока давности)
            )
            logger.debug(f'Отправка успешно запланирована')

        # Отправить сообщение на телефон

        if user.phone:
            # Not implemented
            pass

    # Разослать сообщения пользователям через WebSockets

    logger.debug(f'Производится отправка сообщения для активных подключений по WebSocket...')
    await websockets_manager.broadcast(f'"{message.subject}": "{message.text}"')
    logger.debug(f'OK')


@app.get('/')
async def get():
    """
    Возвращает HTML-страницу для подключения через WebSocket.

    :return:
    """
    logger.debug(f'GET:/')
    return HTMLResponse(html.index_html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Создаёт и обслуживает подключение по WebSocket.

    :param websocket:
    :return:
    """
    logger.debug(f'ws:/ws')

    await websockets_manager.connect(websocket)
    logger.debug(f'Подключён клиент {websocket}')

    while True:
        try:
            data = await websocket.receive()
            logger.debug(f'От клиента {websocket} получены данные: {data}')
            # await websockets_manager.broadcast(f"Client #{websocket} says: {data}")
        except WebSocketDisconnect:
            logger.debug(f'Соединения с клиентом {websocket} завершено')
            websockets_manager.disconnect(websocket)
