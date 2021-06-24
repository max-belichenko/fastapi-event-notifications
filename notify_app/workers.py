import dramatiq

from dramatiq.results.backends import RedisBackend
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from smtplib import SMTPException

from notify_app import config
from notify_app import utils


# Set up Dramatiq

result_backend = RedisBackend()
redis_broker = RedisBroker(host=config.REDIS_HOST, port=config.REDIS_PORT)
redis_broker.add_middleware(Results(backend=result_backend))
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def send_by_email(address: str, message: str):
    """
    Отправляет сообщение на указанный e-mail.

    :param address: E-mail получателя
    :param message: Сообщение
    :return:    "OK"    - В случае успешной отправки
                SMTPException - В случае ошибки
    """
    result = 'OK'
    try:
        utils.send_email.send_text_message(recipient=address, message=message)
    except SMTPException as e:
        result = e

    return result


@dramatiq.actor
def send_sms(phone: str, message: str):
    """
    Отправляет сообщение на указанный номер телефона

    :param phone:   Номер телефона получателя в форматах: +79XXXXXXXXX, 89XXXXXXXXX, 9XXXXXXXXX
    :param message: Сообщение
    :return:
    """
    result = 'NOT IMPLEMENTED'

    return result


@dramatiq.actor
def send_web_notification(user, message):
    """
    Отправляет push-уведомление пользователю

    :param user:    Пользователь с активной сессией
    :param message: Сообщение
    :return:
    """
    result = 'NOT IMPLEMENTED'

    return result
