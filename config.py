# -*- coding: utf-8 -*-
import configparser
import os

config_file = configparser.ConfigParser()
config = config_file['DEFAULT']

current_path = os.path.abspath(os.path.dirname(__file__))
if os.path.exists(current_path + '/' + "config.ini"):
    config_file.read(current_path + '/' + "config.ini")
else:
    config = {
        'TOKEN': 'место для токена',
        'WEBHOOK_HOST': '',
        'WEBHOOK_PORT': '',
        'WEBHOOK_SSL_CERT': '',
        'WEBHOOK_SSL_PRIV': '',
        'DB_NAME': 'название базы данных',
        'DB_HOST': 'адрес БД',
        'DB_USER': 'пользователь для работы с БД',
        'DB_PASSWORD': 'пароль пользователя',
        'LOG_DIR_PATH': current_path + '/' + 'log' + '/',
        'WEEK_TYPE': '0',
        'STATISTIC_TOKEN': ''}
    with open(current_path + '/' + 'config.ini', 'w') as configfile:
        config_file.write(configfile)


daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

ScheduleType = {
    "Понедельник": daysOfWeek[0],
    "Вторник": daysOfWeek[1],
    "Среда": daysOfWeek[2],
    "Четверг": daysOfWeek[3],
    "Пятница": daysOfWeek[4],
    "Суббота": daysOfWeek[5],
    "Воскресенье": daysOfWeek[6],
    "Сегодня": "Today",
    "Завтра": "Tomorrow",
    "Вся неделя": daysOfWeek
}

daysOfWeek_rus = {
    daysOfWeek[0]: "Понедельник",
    daysOfWeek[1]: "Вторник",
    daysOfWeek[2]: "Среда",
    daysOfWeek[3]: "Четверг",
    daysOfWeek[4]: "Пятница",
    daysOfWeek[5]: "Суббота",
    daysOfWeek[6]: "Воскресенье",
}
