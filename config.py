# -*- coding: utf-8 -*-
import configparser
import os

config = configparser.ConfigParser()

current_path = os.path.abspath(os.path.dirname(__file__))
if os.path.exists(current_path + '/' + "config.ini"):
    config.read(current_path + '/' + "config.ini")
else:
    config['DEFAULT'] = {'token': '',
                         'db_path': current_path + '/' + 'base',
                         'log_dir_patch': current_path + '/' + 'log'}
    with open(current_path + '/' + 'config.ini', 'w') as configfile:
        config.write(configfile)

token = config["DEFAULT"]["token"]
db_path = config["DEFAULT"]["db_path"] + "/" + "base.db"
log_dir_patch = config["DEFAULT"]["log_dir_patch"] + "/"
daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

ScheduleType = {
    "Понедельник": daysOfWeek[0],
    "Вторник": daysOfWeek[1],
    "Среда": daysOfWeek[2],
    "Четверг": daysOfWeek[3],
    "Пятница": daysOfWeek[4],
    "Суббота": daysOfWeek[5],
    "Сегодня": "Today",
    "Вся неделя": daysOfWeek
}

daysOfWeek_rus = {
    daysOfWeek[0]: "Понедельник",
    daysOfWeek[1]: "Вторник",
    daysOfWeek[2]: "Среда",
    daysOfWeek[3]: "Четверг",
    daysOfWeek[4]: "Пятница",
    daysOfWeek[5]: "Суббота",
}
