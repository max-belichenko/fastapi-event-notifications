from copy import deepcopy
from random import randint

import pytz

from notify_app.schemas import User


# Создать псевдо-таблицу пользователей

def get_random_timezone() -> str:
    """
    Возвращает произвольную таймзону в текстовом формате
    :return:    Example: "Europe/Moscow"
    """
    timezone_count = len(pytz.all_timezones)
    timezone = pytz.all_timezones[randint(0, timezone_count-1)]
    return timezone


_USERS = [
    User(
        id=i,
        name=f'User #{i}',
        email='max.belichenko@mail.ru',
        phone='79123456789',
        timezone=get_random_timezone()
    )
    for i in range(3)
]


def get_user_list():
    """
    Mock-функция, возвращающая список пользователей.
    """
    return deepcopy(_USERS)


def get_user_by_id(user_id: int):
    """
    Mock-функция, возвращающая пользователя по id.
    """
    for user in _USERS:
        if user.id == user_id:
            break
    else:
        user = None

    return user
