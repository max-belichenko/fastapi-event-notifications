from fastapi import FastAPI

from notify_app import workers


app = FastAPI()


@app.post('/send_message/')
def start_dramatiq_action(subject: str, message: str):
    workers.send_email()