# -*- coding: utf-8 -*-
import re
import sqlite3
from datetime import datetime, time, timedelta

import telebot
from telebot import types

import config
import scheduleCreator

commands = {  # Описание команд используещееся в команде "help"
    'start': 'Стартовое сообщение и предложение зарегистрироваться',
    'help': 'Информация о боте и список доступных команд',
    'registration': 'Выбор ВУЗа, факультета и группы для вывода расписания',
    'send_report <сообщение>': 'Отправить информацию об ошибке или что то ещё'
}

bot = telebot.TeleBot(config.token)

# keyboard
dateSelect = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
button_today = types.KeyboardButton(text="Today")

dateSelect.row("Сегодня")
dateSelect.row("Вся неделя")
dateSelect.row("Понедельник", "Вторник")
dateSelect.row("Среда", "Четверг")
dateSelect.row("Пятница", "Суббота")


# registration

# handle the "/registration" command
@bot.message_handler(commands=['registration'])
def command_registration(m):
    registration("registration:stage 1: none", m.chat.id, m.chat.first_name, m.chat.username)


@bot.callback_query_handler(func=lambda call: True)
def callback_registration(call):
    callback_data = re.split(r':', call.data)
    call_type = callback_data[0]

    if call_type == "registration":
        registration(call.data, call.message.chat.id, call.message.chat.first_name, call.message.chat.username)


def registration(data, cid, name, username):
    # Парсинг сообщения указывающего стадию регистрации
    # registration : stage : org : fac : gr
    callback_data = re.split(r':', data)
    stage = callback_data[1]

    # Процедура регистрации проходит в четрые этапа:
    # 1 этап: выбор учебного заведения
    # 2 этап: выбор факультета
    # 3 этап: выбор группы
    # 4 этап: добавление данных о принадлежности пользователя к учебному заведению в БД
    try:
        con = sqlite3.connect(config.db_path)
        cur = con.cursor()

        if stage == "stage 1":
            keyboard = types.InlineKeyboardMarkup()

            cur.execute('SELECT DISTINCT organization FROM organizations')
            result = cur.fetchall()
            for row in result:
                callback_button = types.InlineKeyboardButton(
                    text=str(row[0]),
                    callback_data="registration:stage 2:{0}".format(str(row[0])))
                keyboard.add(callback_button)

            bot.send_message(cid, "Выберите университет:", reply_markup=keyboard)
        elif stage == "stage 2":
            organization = callback_data[2]
            keyboard = types.InlineKeyboardMarkup()

            cur.execute('SELECT DISTINCT faculty FROM organizations WHERE organization=(?)', [organization])
            result = cur.fetchall()
            for row in result:
                callback_button = types.InlineKeyboardButton(
                    text=str(row[0]),
                    callback_data="registration:stage 3:{0}:{1}".format(organization, str(row[0])))
                keyboard.add(callback_button)

            bot.send_message(cid, "Выберите факультет:", reply_markup=keyboard)
        elif stage == "stage 3":
            organization = callback_data[2]
            faculty = callback_data[3]
            keyboard = types.InlineKeyboardMarkup()
            cur.execute('SELECT id, studGroup FROM organizations WHERE organization=(?) AND faculty=(?)',
                        [organization, faculty])
            result = cur.fetchall()
            for row in result:
                callback_button = types.InlineKeyboardButton(
                    text=str(row[1]),
                    callback_data="registration:stage 4:{0}".format(str(row[0])))
                keyboard.add(callback_button)

            bot.send_message(cid, "Выберите группу:", reply_markup=keyboard)
        elif stage == "stage 4":
            group_id = callback_data[2]

            cur.execute('SELECT tag, studGroup  FROM organizations WHERE id=(?)', [group_id])
            row = cur.fetchall()

            cur.execute('SELECT * FROM users WHERE id = (?)', [cid])
            user = cur.fetchone()
            if user:
                cur.execute('UPDATE users SET scheduleTag = (?) WHERE id = (?)', (str(row[0][0]), cid))
            else:
                cur.execute('INSERT INTO users VALUES(?,?,?,?)', (cid, name, username, str(row[0][0])))
            con.commit()
            con.close()
            bot.send_message(cid, "Отлично, вы зарегистрировались, ваша группа: " + row[0][1]
                             + "\nЕсли вы ошиблись, то просто введиде команду /registration и измените данные",
                             reply_markup=dateSelect)
        else:
            print("unknown stage")
    except:
        bot.send_message(cid, "Сдучилось что-то странное, попробуйте начать сначала, введя команду /registration")


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    command_help(m)

    # bd
    try:
        con = sqlite3.connect(config.db_path)
        cur = con.cursor()
    except sqlite3.Error:
        bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново", reply_markup=dateSelect)
        return None

    cur.execute('SELECT * FROM users WHERE id = (?)', [cid])
    user = cur.fetchone()
    if user:
        bot.send_message(cid, "Вы уже добавлены в базу данных", reply_markup=dateSelect)
    else:
        bot.send_message(cid, "Вас ещё нет в базе данных, поэтому пройдите простую процедуру регистрации")
        registration("registration:stage 1: none", cid, m.chat.first_name, m.chat.username)


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Доступны следующие команды: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text, reply_markup=dateSelect)

    help_text = 'Описание кнопок:\nКнопка "Сегодня", как это ни странно выводит расписание на сегодняшний день, причём с учётом типа недели (числитель/знаменатель), но есть один нюанс: если сегодня воскресенье или время больше чем 21:30, то выводится расписание на следующий день\n'
    bot.send_message(cid, help_text, reply_markup=dateSelect)


# send_report handler
@bot.message_handler(commands=['send_report'])
def command_send_report(m):
    cid = m.chat.id
    data = m.text.split("/send_report")

    if data[1] != '':
        report = data[1]
        try:
            con = sqlite3.connect(config.db_path)
            cur = con.cursor()
            cur.execute('INSERT INTO reports (user_id, report, date) VALUES(?, ?, ?)',
                        [cid, report, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            con.commit()

            bot.send_message(cid, "Сообщение принято")
        except:
            bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново",
                             reply_markup=dateSelect)
    else:
        bot.send_message(cid, "Вы отправили пустую строку", reply_markup=dateSelect)


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
                con = sqlite3.connect(config.db_path)
                cur = con.cursor()
                cur.execute('SELECT scheduleTag FROM users WHERE id = (?)', [cid])
                user = cur.fetchone()
                if user:
                    result = scheduleCreator.create_schedule_text(user[0], day, week_type)
                    for schedule in result:
                        bot.send_message(cid, schedule, reply_markup=dateSelect)
                else:
                    bot.send_message(cid, "Вас ещё нет в базе данных, поэтому пройдите простую процедуру регистрации")
                    registration("registration:stage 1: none", cid, m.chat.first_name, m.chat.username)
            except:
                bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново")
    else:
        bot.send_message(cid, "Неизвестная команда", reply_markup=dateSelect)


bot.polling()
