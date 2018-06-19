import threading
import logging
from datetime import datetime, time, timedelta
from time import sleep

import telebot

from config import config
from helpers import daysOfWeek, get_date_keyboard
from scheduleCreator import create_schedule_text
from scheduledb import ScheduleDB

# Статистика
from statistic import track

bot = telebot.AsyncTeleBot(config["TOKEN"])


logging.basicConfig(format='%(asctime)-15s [ %(levelname)s ] uid=%(userid)s %(message)s',
                    filemode='a',
                    filename=config["LOG_DIR_PATH"] + "log-{0}.log".format(datetime.now().strftime("%Y-%m-%d")),
                    level="INFO")
logger = logging.getLogger('bot-logger')


def auto_posting(current_time):
    today = datetime.now()
    week_type = (today.isocalendar()[1] + int(config["WEEK_TYPE"])) % 2

    if datetime.weekday(today) == 6:
        today += timedelta(days=1)
        week_type = (week_type + 1) % 2

    day = [daysOfWeek[datetime.weekday(today)]]

    # Выборка пользователей из базы у которых установлена отправка расписния на текущий день
    with ScheduleDB(config) as db:
        users = db.find_users_where(auto_posting_time=current_time, is_today=True)

    if users is None:
        return None
    try:
        for user in users:
            cid = user[0]
            tag = user[1]

            schedule = create_schedule_text(tag, day[0], week_type)
            if len(schedule[0]) <= 14:
                continue
            bot.send_message(cid, schedule, reply_markup=get_date_keyboard())

            # Статистика
            if config['STATISTIC_TOKEN'] != '':
                track(config['STATISTIC_TOKEN'], cid, current_time, 'auto_posting')
            else:
                logger.info('auto_posting. Time: {0}'.format(current_time), extra={'userid': cid})
    except BaseException as e:
        logger.warning('auto_posting: {0}'.format(str(e)), extra={'userid': 0})

    # Выборка пользователей из базы у которых установлена отправка расписния на завтрашний день,
    # если сегодня воскресенье, то расписание будет отправляться на понедельник.
    if datetime.weekday(datetime.now()) != 6:
        today += timedelta(days=1)

    day = [daysOfWeek[datetime.weekday(today)]]

    with ScheduleDB(config) as db:
        users = db.find_users_where(auto_posting_time=current_time, is_today=False)

    if users is None:
        return None
    try:
        for user in users:
            cid = user[0]
            tag = user[1]

            schedule = create_schedule_text(tag, day[0], week_type)
            if len(schedule[0]) <= 14:
                continue
            bot.send_message(cid, schedule, reply_markup=get_date_keyboard())

            # Статистика
            if config['STATISTIC_TOKEN'] != '':
                track(config['STATISTIC_TOKEN'], cid, current_time, 'auto_posting')
            else:
                logger.info('auto_posting. Time: {0}'.format(current_time), extra={'userid': cid})
    except BaseException as e:
        logger.warning('auto_posting: {0}'.format(str(e)), extra={'userid': 0})


if __name__ == "__main__":
    while True:
        threading.Thread(target=auto_posting(datetime.now().time().strftime("%H:%M:00"))).start()
        # Вычисляем разницу в секундах, между началом минуты и временем завершения потока
        time_delta = datetime.now() - datetime.now().replace(second=0, microsecond=0)
        # Поток засыпает на время равное количеству секунд до следующей минуты
        sleep(60 - time_delta.seconds)
