# -*- coding: utf-8 -*-
import logging
import re
import threading
from datetime import datetime, time, timedelta
from time import sleep

import telebot
from telebot import types

import config
from scheduleCreator import create_schedule_text
from scheduledb import ScheduleDB, organization_field_length, faculty_field_length

bot = telebot.TeleBot(config.token)

logging.basicConfig(format='%(asctime)-15s [ %(levelname)s ] uid=%(userid)s %(message)s',
                    filemode='a',
                    filename=config.log_dir_patch + "log-{0}.log".format(datetime.now().strftime("%Y-%m")))
logger = logging.getLogger('bot-logger')

commands = {  # Описание команд используещееся в команде "help"
    'start': 'Стартовое сообщение и предложение зарегистрироваться',
    'help': 'Информация о боте и список доступных команд',
    'registration': 'Выбор ВУЗа, факультета и группы для вывода расписания',
    'send_report <сообщение>': 'Отправить информацию об ошибке или что то ещё',
    'auto_posting_on <ЧЧ:ММ>': 'Включение и выбор времени для автоматической отправки расписания в диалог',
    'auto_posting_off': 'Выключение автоматической отправки расписания'
}


def get_date_keyboard():
    date_select = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)

    date_select.row("Сегодня")
    date_select.row("Вся неделя")
    date_select.row("Понедельник", "Вторник")
    date_select.row("Среда", "Четверг")
    date_select.row("Пятница", "Суббота")

    return date_select


# handle the "/registration" command
@bot.message_handler(commands=['registration'])
def command_registration(m):
    registration("reg:stage 1: none", m.chat.id, m.chat.first_name, m.chat.username)


@bot.callback_query_handler(func=lambda call: True)
def callback_registration(call):
    callback_data = re.split(r':', call.data)
    call_type = callback_data[0]

    if call_type == "reg":
        registration(call.data, call.message.chat.id, call.message.chat.first_name, call.message.chat.username)


def registration(data, cid, name, username):
    # Парсинг сообщения указывающего стадию регистрации
    # reg : stage : tag
    callback_data = re.split(r':', data)
    stage = callback_data[1]

    # Процедура регистрации проходит в четрые этапа:
    # 1 этап: выбор учебного заведения
    # 2 этап: выбор факультета
    # 3 этап: выбор группы
    # 4 этап: добавление данных о принадлежности пользователя к учебному заведению в БД
    try:
        db = ScheduleDB()

        if stage == "stage 1":
            keyboard = types.InlineKeyboardMarkup()

            result = db.get_organizations()
            for row in result:
                callback_button = types.InlineKeyboardButton(
                    text=str(row[0]),
                    callback_data="reg:stage 2:{0}".format(str(row[1])[:organization_field_length]))
                keyboard.add(callback_button)

            bot.send_message(cid, "Выберите университет:", reply_markup=keyboard)
        elif stage == "stage 2":
            keyboard = types.InlineKeyboardMarkup()

            organization_id = callback_data[2]
            result = db.get_faculty(organization_id)
            for row in result:
                callback_button = types.InlineKeyboardButton(
                    text=str(row[0]),
                    callback_data="reg:stage 3:{0}".format(
                        str(row[1])[:organization_field_length + faculty_field_length]))
                keyboard.add(callback_button)

            bot.send_message(cid, "Выберите факультет:", reply_markup=keyboard)
        elif stage == "stage 3":
            keyboard = types.InlineKeyboardMarkup()

            faculty_id = callback_data[2]
            result = db.get_group(faculty_id)
            for row in result:
                callback_button = types.InlineKeyboardButton(
                    text=str(row[0]),
                    callback_data="reg:stage 4:{0}".format(str(row[1])))
                keyboard.add(callback_button)

            bot.send_message(cid, "Выберите группу:", reply_markup=keyboard)
        elif stage == "stage 4":
            group_id = callback_data[2]
            row = db.get_group(group_id)

            user = db.find_user(cid)
            if user:
                db.update_user(cid, name, username, str(row[0][1]))
            else:
                db.add_user(cid, name, username, str(row[0][1]))

            bot.send_message(cid, "Отлично, вы зарегистрировались, ваша группа: " + row[0][0]
                             + "\nЕсли вы ошиблись, то просто введиде команду /registration и измените данные",
                             reply_markup=get_date_keyboard())
            bot.send_message(cid, "Теперь вы можете настроить автоматическую отправку расписания в заданное вами время,"
                                  " введя команду /auto_posting_on <время>, "
                                  "где <время> должно иметь формат ЧЧ:ММ")
        else:
            print("unknown stage")
    except BaseException as e:
        logger.warning('Registration problem: {0}'.format(str(e)), extra={'userid': cid})
        bot.send_message(cid, "Случилось что-то странное, попробуйте начать сначала, введя команду /registration")


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    command_help(m)

    try:
        with ScheduleDB() as db:
            user = db.find_user(cid)
        if user:
            bot.send_message(cid, "Вы уже добавлены в базу данных", reply_markup=get_date_keyboard())
        else:
            bot.send_message(cid, "Вас ещё нет в базе данных, поэтому пройдите простую процедуру регистрации")
            registration("registration:stage 1: none", cid, m.chat.first_name, m.chat.username)
    except BaseException as e:
        logger.warning('command start: {0}'.format(str(e)), extra={'userid': cid})
        bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново",
                         reply_markup=get_date_keyboard())


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Доступны следующие команды: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text, reply_markup=get_date_keyboard())

    help_text = ('Описание кнопок:\nКнопка "Сегодня", как это ни странно выводит расписание на сегодняшний день, '
                 'причём с учётом типа недели (числитель/знаменатель), но есть один нюанс: если сегодня воскресенье '
                 'или время больше чем 21:30, то выводится расписание на следующий день\n')
    bot.send_message(cid, help_text, reply_markup=get_date_keyboard())
    
    guide_url = 'https://github.com/paladin-705/UniversityScheduleBot/wiki/Guide'

    help_text = 'Более подробную инструкцию и описание команд (с инструкциями гифками! ^_^) вы можете посмотерть по ссылке: {}'.format(guide_url)
    bot.send_message(cid, help_text, reply_markup=get_date_keyboard())


# send_report handler
@bot.message_handler(commands=['send_report'])
def command_send_report(m):
    cid = m.chat.id
    data = m.text.split("/send_report")

    if data[1] != '':
        report = data[1]
        with ScheduleDB() as db:
            if db.add_report(cid, report):
                bot.send_message(cid, "Сообщение принято")
            else:
                bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново",
                                 reply_markup=get_date_keyboard())
    else:
        bot.send_message(cid, "Вы отправили пустую строку", reply_markup=get_date_keyboard())


# handle the "/start" command
@bot.message_handler(commands=['auto_posting_on'])
def command_auto_posting_on(m):
    cid = m.chat.id

    try:
        data = m.text.split("/auto_posting_on")[1].strip()
        if re.match(data, r'\d{1,2}:\d\d'):
            raise BaseException
    except:
        bot.send_message(cid, "Вы отправили пустую строку или строку неправильного формата. Правильный формат ЧЧ:ММ",
                         reply_markup=get_date_keyboard())
        return None

    try:
        db = ScheduleDB()
        user = db.find_user(cid)
        if user:
            if db.set_auto_post_time(cid, (data + ":00").rjust(8, '0')):
                bot.send_message(cid, "Время установлено")
            else:
                bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново",
                                 reply_markup=get_date_keyboard())
        else:
            bot.send_message(cid, "Вас ещё нет в базе данных, поэтому пройдите простую процедуру регистрации")
            registration("registration:stage 1: none", cid, m.chat.first_name, m.chat.username)
    except BaseException as e:
        logger.warning('command auto_posting_on: {0}'.format(str(e)), extra={'userid': cid})
        bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново")


@bot.message_handler(commands=['auto_posting_off'])
def command_auto_posting_off(m):
    cid = m.chat.id

    try:
        db = ScheduleDB()
        user = db.find_user(cid)
        if user:
            if db.set_auto_post_time(cid, ""):
                bot.send_message(cid, "Автоматическая отправка расписания успешно отключена")
            else:
                bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново",
                                 reply_markup=get_date_keyboard())
        else:
            bot.send_message(cid, "Вас ещё нет в базе данных, поэтому пройдите простую процедуру регистрации")
            registration("registration:stage 1: none", cid, m.chat.first_name, m.chat.username)
    except BaseException as e:
        logger.warning('command auto_posting_off: {0}'.format(str(e)), extra={'userid': cid})
        bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново")


# text message handler
@bot.message_handler(func=lambda message: True, content_types=['text'])
def response_msg(m):
    cid = m.chat.id
    if m.text in config.ScheduleType:
        # По умолчанию week_type равен -1 и при таком значении будут выводится все занятия, 
        # т.е и для чётных и для нечётных недель
        week_type = -1

        if m.text == "Вся неделя":
            days = config.ScheduleType[m.text]
        elif m.text == "Сегодня":
            today = datetime.now()
            # Если запрашивается расписание на сегодняшний день, 
            # то week_type равен остатку от деления на 2 номера недели в году, т.е он определяет чётная она или нечётная
            week_type = today.isocalendar()[1] % 2

            # Если время больше чем 21:30, то показываем расписание на следующий день
            if today.time() >= time(21, 30):
                today += timedelta(days=1)

            # Если сегодня воскресенье, то показывается расписание на понедельник следующей недели
            # Также в этом случае, как week_type используется тип следующей недели
            if datetime.weekday(today) == 6:
                today += timedelta(days=1)
                week_type = (week_type + 1) % 2

            days = [config.daysOfWeek[datetime.weekday(today)]]
        else:
            days = [config.ScheduleType[m.text]]

        for day in days:
            try:
                with ScheduleDB() as db:
                    user = db.find_user(cid)
                if user:
                    result = create_schedule_text(user[0], day, week_type)
                    for schedule in result:
                        bot.send_message(cid, schedule, reply_markup=get_date_keyboard())
                else:
                    bot.send_message(cid, "Вас ещё нет в базе данных, поэтому пройдите простую процедуру регистрации")
                    registration("registration:stage 1: none", cid, m.chat.first_name, m.chat.username)
            except BaseException as e:
                logger.warning('response_msg: {0}'.format(str(e)), extra={'userid': cid})
                bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново")
    else:
        bot.send_message(cid, "Неизвестная команда", reply_markup=get_date_keyboard())


def auto_posting(current_time):
    today = datetime.now()
    week_type = today.isocalendar()[1] % 2

    if today.time() >= time(21, 30):
        today += timedelta(days=1)

    if datetime.weekday(today) == 6:
        today += timedelta(days=1)
        week_type = (week_type + 1) % 2

    day = [config.daysOfWeek[datetime.weekday(today)]]

    with ScheduleDB() as db:
        users = db.find_users_where(auto_posting_time=current_time)

    if users is None:
        return None
    try:
        for user in users:
            cid = user[0]
            tag = user[1]

            schedule = create_schedule_text(tag, day[0], week_type)
            bot.send_message(cid, schedule, reply_markup=get_date_keyboard())
    except BaseException as e:
        logger.warning('auto_posting: {0}'.format(str(e)))


def auto_posting_thread():
    while True:
        auto_posting(datetime.now().time().strftime("%H:%M:00"))
        sleep(60)


def main():
    # auto posting thread
    threading.Thread(target=auto_posting_thread).start()

    # bot polling
    bot.polling()


if __name__ == "__main__":
    main()
