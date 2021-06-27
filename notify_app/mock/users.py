from copy import deepcopy
from random import randint

import pytz

from notify_app.schemas import UserDBSchema


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
    UserDBSchema(
        id=i,
        name=f'User #{i}',
        email='max.belichenko@mail.ru',
        phone='79123456789',
        timezone=get_random_timezone()
    )
    for i in range(3)
]
_USERS.append(
    UserDBSchema(
        id=4,
        name=f'Max from Miami',
        email='max.belichenko@mail.ru',
        phone='79123456789',
        timezone='US/Pacific'
    )
)
_USERS.append(
    UserDBSchema(
        id=5,
        name=f'Denis from London',
        email='max.belichenko@mail.ru',
        phone='79123456789',
        timezone='Europe/London'
    )
)
_USERS.append(
    UserDBSchema(
        id=6,
        name=f'Konstantin from Vladik',
        email='max.belichenko@mail.ru',
        phone='79123456789',
        timezone='Asia/Vladivostok'
    )
)

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
