from sqlalchemy.orm import Session

from notify_app.models import Message
from notify_app.schemas import MessageSchema


async def create_message(db: Session, message: MessageSchema):
    """
    Создаёт запись о сообщении в базе данных.

    :param db:
    :param message:
    :return:    Созданный объект сообщения
    """

    db_message = Message(subject=message.subject, text=message.text, send_date=message.send_date)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message
