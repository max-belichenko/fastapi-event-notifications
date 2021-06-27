import datetime

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


# Send message configuration

SERVER_TIMEZONE_STR = 'Europe/Moscow'

SEND_ALLOWED_PERIOD = (
    datetime.time(9, 0),    # Начало рассылки в 9:00
    datetime.time(21, 0),   # Окончание рассылки в 21:00
)


# WebSocket configuration

WEBSOCKET_SERVER = '*'
WEBSOCKET_PORT = '*'
WEBSOCKET_URL = 'ws'


# Redis server configuration

REDIS_HOST = "*"
REDIS_PORT = 6379


# SMTP server configuration

SMTP_SERVER_HOSTNAME = '*'
SMTP_SERVER_PORT = 465
SMTP_USER = '*'
SMTP_PASSWORD = '*'
SMTP_FROM_ADDRESS = '*'


# Database configuration

DB_CONNECTION_URL = 'sqlite:///./notify_app.db'
DB_SCHEDULER_URL = 'sqlite:///./scheduler.db'


# Scheduler configuration

SCHEDULER_CONFIG = {
    'jobstores': {
        'default': SQLAlchemyJobStore(url=DB_SCHEDULER_URL)     # Store jobs in database
    },
    'executors': {
        'default': ThreadPoolExecutor(20),  # Run jobs in threads
    },
    'job_defaults': {
        'coalesce': False,
        'max_instances': 3
    },
    # 'timezone': pytz.utc,   # Use UTC timezones for scheduling
}


# Logger config

LOG_FORMAT = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
LOG_FILENAME = 'notify_app.log'
