# -*- coding: utf-8 -*-
import telebot
from telebot import types

from datetime import datetime, date, time
#import time

import sqlite3
import re
import hashlib

import config
import scheduleCreator

commands = {  # command description used in the "help" command
              'start': 'Стартовое сообщение и предложение зарегистрироваться',
              'help': 'Информация о боте и список доступных команд',
              'registration': 'Выбор ВУЗа, факультета и группы для вывода расписания',
              'send_report <сообщение>': 'Отправить информацию об ошибке или что то ещё' 
}

bot = telebot.TeleBot(config.token)

#keyboard
dateSelect = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
button_today = types.KeyboardButton(text="Today")

dateSelect.row("Сегодня")
dateSelect.row("Вся неделя")
dateSelect.row("Понедельник","Вторник")
dateSelect.row("Среда","Четверг")
dateSelect.row("Пятница","Суббота")


#registration

# handle the "/registration" command
@bot.message_handler(commands=['registration'])
def command_registration(m):
    registration("registration:stage 1: none", m.chat.id, m.chat.first_name, m.chat.username)
    
@bot.callback_query_handler(func=lambda call: True)
def callback_registration(call):
    callbackData = re.split(r':', call.data)
    callType = callbackData[0]
    
    if callType == "registration":
        registration(call.data, call.message.chat.id, call.message.chat.first_name, call.message.chat.username)

def registration(data, cid, name, username):
    #parse message
    #stage : org : fac : gr 
    callbackData = re.split(r':', data)
    stage = callbackData[1]

    try:
        con = sqlite3.connect(config.db_path)
        cur = con.cursor()

        if stage == "stage 1":
            keyboard = types.InlineKeyboardMarkup()
                
            cur.execute('SELECT DISTINCT organization FROM organizations')
            result = cur.fetchall()
            for row in result:
                callback_button = types.InlineKeyboardButton(text=str(row[0]), callback_data="registration:stage 2:{0}".format(str(row[0])))
                keyboard.add(callback_button)
                
            bot.send_message(cid, "Выберите университет:", reply_markup=keyboard)
        elif stage == "stage 2":
            organization = callbackData[2]
            keyboard = types.InlineKeyboardMarkup()
            
            cur.execute('SELECT DISTINCT faculty FROM organizations WHERE organization=(?)', [organization])
            result = cur.fetchall()
            for row in result:
                callback_button = types.InlineKeyboardButton(text=str(row[0]), callback_data="registration:stage 3:{0}:{1}".format(organization, str(row[0])))
                keyboard.add(callback_button)
            
            bot.send_message(cid, "Выберите факультет:", reply_markup=keyboard) 
        elif stage == "stage 3":
            organization = callbackData[2]
            faculty = callbackData[3]
            keyboard = types.InlineKeyboardMarkup()
            cur.execute('SELECT id, studGroup FROM organizations WHERE organization=(?) AND faculty=(?)', [organization, faculty])
            result = cur.fetchall()
            for row in result:
                callback_button = types.InlineKeyboardButton(text=str(row[1]), callback_data="registration:stage 4:{0}".format(str(row[0])))
                keyboard.add(callback_button)
            
            bot.send_message(cid, "Выберите группу:", reply_markup=keyboard)
        elif stage == "stage 4":
            groupId = callbackData[2]
            
            cur.execute('SELECT tag, studGroup  FROM organizations WHERE id=(?)', [groupId])
            row = cur.fetchall()

            cur.execute('SELECT * FROM users WHERE id = (?)', [cid])
            user = cur.fetchone()
            if user:
                cur.execute('UPDATE users SET scheduleTag = (?) WHERE id = (?)',(str(row[0][0]), cid))
            else:
                cur.execute('INSERT INTO users VALUES(?,?,?,?)',(cid, name, username, str(row[0][0])))
            con.commit()
            con.close()
            bot.send_message(cid, "Отлично, вы зарегистрировались, ваша группа: " + row[0][1] + "\nЕсли вы ошиблись, то просто введиде команду /registration и измените данные", reply_markup=dateSelect)
        else:
            print("unknown stage")
    except:
        bot.send_message(cid, "Сдучилось что-то странное, попробуйте начать сначала, введя команду /registration")
    
# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    command_help(m)
    
    #bd
    try:
        con = sqlite3.connect(config.db_path)
        cur = con.cursor()
    except sqlite3.Error:
        sys.exit(1)

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
    data = (m.text).split("/send_report")
    
    if data[1] != '':
        report = data[1]
        try:
            con = sqlite3.connect(config.db_path)
            cur = con.cursor()
            cur.execute('INSERT INTO reports (user_id, report) VALUES(?, ?)', [cid, report])
            con.commit()
            
            bot.send_message(cid, "Сообщение принято")
        except:
            bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново", reply_markup=dateSelect)
    else:
        bot.send_message(cid, "Вы отправили пустую строку", reply_markup=dateSelect)
        
# text message handler
@bot.message_handler(func=lambda message: True, content_types=['text'])
def response_msg(m):
    cid = m.chat.id
    if m.text in config.ScheduleType:
        week_type = -1                          #По умолчанию week_type равен -1 и при таком значении будут выводится все занятия, т.е и для чётных и для нечётных недель
        
        if(m.text == "Вся неделя"):
            days = config.ScheduleType[m.text]
        elif(m.text == "Сегодня"):
            today = datetime.now()
            week_type = today.isocalendar()[1]%2            #если запрашивается расписание на сегодняшний день, то week_type равен остатку от деления на 2 номера недели в году, т.е он определяет чётная она или нечётная
            
            if(datetime.weekday(today) == 6 or today.time() >= time(21,30)):
                days = [config.daysOfWeek[(datetime.weekday(today)+1)%7]]
            else:
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
                    result = scheduleCreator.createSchedule_text(user[0], day, week_type)
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

