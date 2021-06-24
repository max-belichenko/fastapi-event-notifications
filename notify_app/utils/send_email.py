import datetime
import smtplib

from notify_app import config


def send_text_message(recipient: str, subject: str = '', message: str = ''):
    """
    Отправляет текстовое сообщение на указанный e-mail.

    :param recipient:   E-mail получателя
    :param subject:     Тема сообщения
    :param message:     Текст сообщения
    :return:
    """
    from_address = config.SMTP_FROM_ADDRESS
    message_dt = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

    msg = f'From: {from_address}\r\n' \
          f'To: {recipient}\r\n' \
          f'Subject: {subject}\r\n' \
          f'Date: {message_dt}\r\n\r\n' \
          f'{message}'

    connection = smtplib.SMTP_SSL(host=config.SMTP_SERVER_HOSTNAME, port=config.SMTP_SERVER_PORT)
    connection.login(user=config.SMTP_USER, password=config.SMTP_PASSWORD)
    connection.sendmail(from_addr=from_address, to_addrs=recipient, msg=msg)
    connection.quit()
