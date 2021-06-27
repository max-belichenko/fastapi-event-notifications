import dramatiq

from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results

from notify_app import config
from notify_app.utils import send_email
from notify_app.web_service import websockets_manager


# Set up Dramatiq

result_backend = RedisBackend()
redis_broker = RedisBroker(host=config.REDIS_HOST, port=config.REDIS_PORT)
redis_broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def send_by_email(address: str, message: str, subject: str = ''):
    """
    Отправляет сообщение на указанный e-mail.

    В случае возникновения исключения - повторяет отправку.
    (настройка повторной отправки производится с помощью модуля dramatiq.middleware.retries)

    :param address: E-mail получателя
    :param subject: Тема сообщения
    :param message: Сообщение
    :return:
    """
    send_email.send_text_message(recipient=address, message=message, subject=subject)


@dramatiq.actor
def send_sms(phone: str, message: str):
    """
    Отправляет сообщение на указанный номер телефона

    :param phone:   Номер телефона получателя в форматах: +79XXXXXXXXX, 89XXXXXXXXX, 9XXXXXXXXX
    :param message: Сообщение
    :return:
    """
    raise NotImplementedError('Функция отправки SMS-сообщения не реализована')


@dramatiq.actor
def send_web_notification(subject: str, text: str):
    """
    Отправляет push-уведомление пользователям.

    :param webscokets:
    :param subject:
    :param text:
    :return:
    """
    raise NotImplementedError('Функция отправки push-уведомления не реализована')
