from typing import Tuple

import datetime

import pytz


def add_timezone_if_empty(dt: datetime.datetime, timezone: str):
    """
    Добавляет к объекту datetime.datetime указанную временную зону. Время при этом не меняется и считается, что оно
    задано в указанной временной зоне.
    Если временная зона уже задана, то она не меняется и временной объект возвращается без изменений.

    :param dt:          Объект, содержащий дату и время
    :param timezone:    Временная зона в текстовом формате. Например: "Europe/Moscow"
    :return:            Объект, содержащий дату, время и временную зону
    """
    tz = pytz.timezone(timezone)

    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return tz.localize(dt)
    else:
        return dt


def get_send_dt_for_user(send_date, user_timezone, allowed_period: Tuple[datetime.time, datetime.time]):
    """
    Вычисляет ближайшее возможное время отправки уведомления для пользователя в соотвествии с:
        Локальной таймзоной сервера;
        Таймзоной пользователя;
        Временным интервалом доставки уведомлений.

    :param send_date:       Время запланированной отправки на сервере
    :param user_timezone:   Таймзона пользователя. Например: 'Europe/Moscow'    # +3:00
    :param allowed_period:  Интервал доставки уведомлений в формате (datetime, datetime). Например:
                            ((9, 0), (2021, 06, 26, 21, 0))
    :return:                <datetime.datetime> - Дата и время отправки, соответствующие разрешённому интервалу
    """
    print('Устанавливаю время отправки в соответсвии с разрешённым временным интервалом:')
    # Проверить, установлена ли временная зона для даты и времени запланированной отправки сообщения

    if send_date.tzinfo is None or send_date.tzinfo.utcoffset(send_date) is None:
        raise ValueError(f'Error! Attribute send_date has no timezone set.\n'
                         f'To provide a timezone, you can use this example:\n'
                         f'send_date = pytz.timezone(<TimeZone: str>).localize(send_date)')

    # Определить временную зону пользователя

    try:
        user_tz = pytz.timezone(user_timezone)
        print(f'Определена временная зона пользователя: {user_tz}')
    except pytz.exceptions.UnknownTimeZoneError as e:
        raise ValueError(f'Error! Unknown user timezone provided: "{user_timezone}"\n'
                         f'You can see the list of timezones by calling pytz.all_timezones')

    # Получить время отправки, локализированные для временной зоны пользователя

    user_dt = send_date.astimezone(user_tz)
    print(f'Определено локальное время отправки: {user_dt}')

    # Установить время отправки сообщения в соответствии с разрешённым временным интервалом

    if user_dt.time() < allowed_period[0]:
        send_dt_for_user = user_dt.replace(hour=allowed_period[0], minute=0).astimezone(send_date.tzinfo)
        print('Время отправки ранее разрешённого временного интервала')
    elif user_dt.time() > allowed_period[1]:
        send_dt_for_user = user_dt.replace(day=user_dt.day+1, hour=allowed_period[0], minute=0).astimezone(send_date.tzinfo)
        print('Время отправки позднее разрешённого временного интервала')
    else:
        send_dt_for_user = send_date

    print(f'Новое время отправки на сервере: {send_dt_for_user}')
    return send_dt_for_user
