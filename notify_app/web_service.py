from fastapi import FastAPI

from notify_app import schemas, workers
from notify_app.mock import users

app = FastAPI()


@app.post('/send_message/')
def start_dramatiq_action(message: schemas.Message):
    """
    URI, предоставляющий функционал для рассылки сообщения.

    :param message: Сообщение в формате
        {
            'subject': <subject: Optional[str]=''>,
            'text': <text: str>
        }
    :return:
    """
    user_list = users.get_user_list()

    for user in user_list:
        if user.email:
            workers.send_by_email(address=user.email, message=message.text, subject=message.subject)
