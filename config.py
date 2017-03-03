# -*- coding: utf-8 -*-
token = ''
db_path = 'base/base.db'

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
