from telebot import types
import datetime

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


def get_date_keyboard():
    now = datetime.datetime.now()

    date_select = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)

    # Если сейчас декабрь, январь или май, июнь, то выводится кнопка экзамены
    if now.month == 1 or now.month == 12 or now.month == 5 or now.month == 6:
        date_select.row('Экзамены')

    date_select.row("Сегодня")
    date_select.row("Завтра")
    date_select.row("Вся неделя")
    date_select.row("Понедельник", "Вторник")
    date_select.row("Среда", "Четверг")
    date_select.row("Пятница", "Суббота")

    return date_select