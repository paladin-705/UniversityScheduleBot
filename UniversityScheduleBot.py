# -*- coding: utf-8 -*-
import telebot
from telebot import types
import time

import sqlite3
import re
import hashlib

import config

commands = {  # command description used in the "help" command
              'start': 'Get used to the bot',
              'help': 'Gives you information about the available commands'
}

def createSchedule(tag, day, type):
    print("foobar")

bot = telebot.TeleBot(config.token)
#bot.set_update_listener(listener)  # register listener

#keyboard
dateSelect = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
button_today = types.KeyboardButton(text="Today")

dateSelect.row("Сегодня")
dateSelect.row("Вся неделя")
dateSelect.row("Понедельник","Вторник")
dateSelect.row("Среда","Четверг")
dateSelect.row("Пятница","Суббота")


#registration
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
        con = sqlite3.connect('base/base.db')
        cur = con.cursor()
    except sqlite3.Error:
        sys.exit(1)
    
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
        
        cur.execute('SELECT tag FROM organizations WHERE id=(?)', [groupId])
        row = cur.fetchall()
        
        cur.execute('INSERT INTO users VALUES(?,?,?,?)',(cid, name, username, str(row[0][0])))
        con.commit()
        con.close()
        bot.send_message(cid, "Отлично, вы зарегистрировались", reply_markup=dateSelect)
    else:
        print("foobar")
    
    
# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id

    #bd
    try:
        con = sqlite3.connect('base/base.db')
        cur = con.cursor()
        #cur.execute("CREATE TABLE users(id INT, name TEXT, username TEXT, hash TEXT);")
    except sqlite3.Error:
        sys.exit(1)

    cur.execute('SELECT * FROM users WHERE id = (?)', [cid])
    user = cur.fetchone()
    if user:
        bot.send_message(cid, "Вы уже добавлены в базу данных", reply_markup=dateSelect)
    else:
        #groupSelect = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        #groupSelect.row("1 Группа", "2 Группа")
        registration("registration:stage 1: none", cid, m.chat.first_name, m.chat.username)
        
        #command_help(m)

# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text, reply_markup=dateSelect)  # send the generated help page

@bot.message_handler(func=lambda message: True, content_types=['text'])
def response_msg(m):
    if(m.text == "1 Группа" or m.text == "2 Группа"):
        try:
            con = sqlite3.connect('base/base.db')
            cur = con.cursor()
            cur.execute('UPDATE users SET hash = (?) WHERE id = (?)',(hashlib.sha256(m.text.encode('utf-8')).hexdigest(), m.chat.id))
            con.commit()
            con.close()
        except sqlite3.Error:
            sys.exit(1)
        bot.send_message(m.chat.id, "Регистрация закончена", reply_markup=dateSelect)
        
    elif m.text in config.ScheduleType:
        if config.ScheduleType[m.text] == "Today":
                bot.send_message(m.chat.id, "Сегодня", reply_markup=dateSelect)
        elif config.ScheduleType[m.text] == "All week":
                bot.send_message(m.chat.id, "Вся неделя", reply_markup=dateSelect)
                for day in config.daysOfWeek:
                    print(day)
        else:
                bot.send_message(m.chat.id, "1 - Инженерная и компьютерная графика лаб. 1-131\n 2 - Неорган. химия лаб. 1-131\n 3 - Неорган. химия лаб. 3-455", reply_markup=dateSelect)
    else:
        bot.send_message(m.chat.id, "Неизвестная команда", reply_markup=dateSelect)
            
bot.polling()

