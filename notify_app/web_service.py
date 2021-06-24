from fastapi import FastAPI

from notify_app import workers


app = FastAPI()


@app.post('/send_message/')
def start_dramatiq_action(message: str, subject: str = None):
    """
    URI, предоставляющий функционал для рассылки сообщения.

    :param message: Текст сообщения
    :param subject: Тема сообщения
    :return:
    """
    workers.send_by_email(message=message, subject=subject if subject else '')
