from sqlalchemy import Column, Integer, String, DateTime, Text, Date
from sqlalchemy.sql import func

from notify_app.database import Base


class Message(Base):
    """
    Описывает модель данных сообщения для рассылки пользователям.
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    subject = Column(String(255))
    text = Column(Text)
    send_date = Column(DateTime(timezone=True))

    def __repr__(self):
        return f'<Message(' \
               f'id={self.id}, ' \
               f'time_created={self.time_created}, ' \
               f'send_date={self.send_date}, ' \
               f'title={self.title}, ' \
               f'message={self.message[:30] if self.message else ""})>'

    def __str__(self):
        return f'[{self.id}] ' \
               f'"{self.title}": ' \
               f'"{self.message[:100]}"'
