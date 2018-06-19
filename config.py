# -*- coding: utf-8 -*-
import configparser
import os

config_file = configparser.ConfigParser()
config = config_file['DEFAULT']

current_path = os.path.abspath(os.path.dirname(__file__))
config_file.read(current_path + '/' + "config.ini")

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
