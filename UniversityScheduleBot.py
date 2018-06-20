# -*- coding: utf-8 -*-
import logging
import re
from datetime import datetime, time, timedelta

import flask
import telebot
from telebot import types

from config import config
from helpers import daysOfWeek, ScheduleType, get_date_keyboard
from scheduleCreator import create_schedule_text
from scheduledb import ScheduleDB, organization_field_length, faculty_field_length

# Статистика
from statistic import track

WEBHOOK_URL_BASE = "https://{}:{}".format(config["WEBHOOK_HOST"], config["WEBHOOK_PORT"])
WEBHOOK_URL_PATH = "/{}/".format(config["TOKEN"])

bot = telebot.AsyncTeleBot(config["TOKEN"])
app = flask.Flask(__name__)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

commands = {  # Описание команд используещееся в команде "help"
    'start': 'Стартовое сообщение и предложение зарегистрироваться',
    'help': 'Информация о боте и список доступных команд',
    'registration': 'Выбор ВУЗа, факультета и группы для вывода расписания',
    'send_report <сообщение>': 'Отправить информацию об ошибке или что то ещё',
    'auto_posting_on <ЧЧ:ММ>': 'Включение и выбор времени для автоматической отправки расписания в диалог',
    'auto_posting_off': 'Выключение автоматической отправки расписания'
}

# -------------------------------------
#  BOT HANDLERS
# -------------------------------------


# handle the "/registration" command
@bot.message_handler(commands=['registration'])
def command_registration(m):
    cid = m.chat.id

    # Процедура регистрации проходит в четрые этапа:
    # 1 этап: выбор учебного заведения <--
    # 2 этап: выбор факультета
    # 3 этап: выбор группы
    # 4 этап: добавление данных о принадлежности пользователя к учебному заведению в БД
    try:
        # Статистика
        if config['STATISTIC_TOKEN'] != '':
            track(config['STATISTIC_TOKEN'], cid, 'stage 1', 'registration-stage-1')

        keyboard = types.InlineKeyboardMarkup()

        with ScheduleDB(config) as db:
            result = db.get_organizations()
        for row in result:
            callback_button = types.InlineKeyboardButton(
                text=str(row[0]),
                callback_data="reg:stage 2:{0}".format(str(row[1])[:organization_field_length]))
            keyboard.add(callback_button)

        bot.send_message(cid, "Выберите университет:", reply_markup=keyboard)
    except BaseException as e:
        logger.warning('Registration problem: {0}'.format(str(e)))
        bot.send_message(cid, "Случилось что-то странное, попробуйте начать сначала, введя команду /registration")


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    # Статистика
    if config['STATISTIC_TOKEN'] != '':
        track(config['STATISTIC_TOKEN'], m.chat.id, m.text, 'start')
    else:
        logger.info('start')

    cid = m.chat.id
    command_help(m)

    try:
        with ScheduleDB(config) as db:
            user = db.find_user(cid)
        if user and user[0] != "":
            bot.send_message(cid, "Вы уже добавлены в базу данных", reply_markup=get_date_keyboard())
        else:
            bot.send_message(cid, "Вас ещё нет в базе данных, поэтому пройдите простую процедуру регистрации")
            command_registration(m)
    except BaseException as e:
        logger.warning('command start: {0}'.format(str(e)))
        bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново",
                         reply_markup=get_date_keyboard())


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    # Статистика
    if config['STATISTIC_TOKEN'] != '':
        track(config['STATISTIC_TOKEN'], m.chat.id, m.text, 'help')
    else:
        logger.info('help')

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

    help_text = 'Более подробную инструкцию и описание команд (с инструкциями гифками! ^_^) \
    вы можете посмотреть по ссылке: {}'.format(guide_url)
    bot.send_message(cid, help_text, reply_markup=get_date_keyboard())


# send_report handler
@bot.message_handler(commands=['send_report'])
def command_send_report(m):
    # Статистика
    if config['STATISTIC_TOKEN'] != '':
        track(config['STATISTIC_TOKEN'], m.chat.id, m.text, 'report')
    else:
        logger.info('report')

    cid = m.chat.id
    data = m.text.split("/send_report")

    if data[1] != '':
        report = data[1]
        with ScheduleDB(config) as db:
            if db.add_report(cid, report):
                bot.send_message(cid, "Сообщение принято")
            else:
                bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново",
                                 reply_markup=get_date_keyboard())
    else:
        bot.send_message(
            cid,
            "Вы отправили пустую строку. Пример: /send_report <сообщение>",
            reply_markup=get_date_keyboard())


# handle the "/auto_posting_on" command
@bot.message_handler(commands=['auto_posting_on'])
def command_auto_posting_on(m):
    # Статистика
    if config['STATISTIC_TOKEN'] != '':
        track(config['STATISTIC_TOKEN'], m.chat.id, m.text, 'auto_posting_on')
    else:
        logger.info('auto_posting_on')

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
        db = ScheduleDB(config)
        user = db.find_user(cid)
        if user and user[0] != "":
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(
                text="На Сегодня",
                callback_data="ap:{0}:1".format(data))
            keyboard.add(callback_button)
            callback_button = types.InlineKeyboardButton(
                text="На Завтра",
                callback_data="ap:{0}:0".format(data))
            keyboard.add(callback_button)

            bot.send_message(cid, "Выберите день на который будет приходить расписание:", reply_markup=keyboard)
        else:
            bot.send_message(cid, "Вас ещё нет в базе данных, поэтому пройдите простую процедуру регистрации")
            command_registration(m)
    except BaseException as e:
        logger.warning('command auto_posting_on: {0}'.format(str(e)))
        bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново")


@bot.message_handler(commands=['auto_posting_off'])
def command_auto_posting_off(m):
    # Статистика
    if config['STATISTIC_TOKEN'] != '':
        track(config['STATISTIC_TOKEN'], m.chat.id, m.text, 'auto_posting_off')
    else:
        logger.info('auto_posting_off')

    cid = m.chat.id

    try:
        db = ScheduleDB(config)
        user = db.find_user(cid)
        if not user:
            bot.send_message(cid, "Вас ещё нет в базе данных, поэтому пройдите простую процедуру регистрации")
            command_registration(m)
            return

        if db.set_auto_post_time(cid, None, None):
            bot.send_message(cid, "Автоматическая отправка расписания успешно отключена")
        else:
            bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново",
                             reply_markup=get_date_keyboard())

    except BaseException as e:
        logger.warning('command auto_posting_off: {0}'.format(str(e)))
        bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново")


# exams message handler
@bot.message_handler(func=lambda message: 'Экзамены' in message.text, content_types=['text'])
def exams(m):
    cid = m.chat.id

    # Статистика
    track(config['STATISTIC_TOKEN'], cid, m.text, 'exams')

    # Если пользователя нет в базе, то ему выведет предложение зарегистрироваться
    try:
        with ScheduleDB(config) as db:
            user = db.find_user(cid)
        if not user or user[0] == '':
            message = "Вас ещё нет в базе данных, поэтому пройдите простую процедуру регистрации:\n"
            message += 'Введите команду(без кавычек):\n\nрегистрация "название вуза" "факультет" "группа"\n\n'
            message += 'Если вы допустите ошибку, то просто наберите команду заново.\n'

            bot.send_message(cid, message, reply_markup=get_date_keyboard())
    except BaseException as e:
        bot.send_message(cid, 'Случилось что то странное, попробуйте ввести команду заново',
                         reply_markup=get_date_keyboard())

    try:
        with ScheduleDB(config) as db:
            exams_list = db.get_exams(user[0])

        message = ''
        for exam in exams_list:
            message += exam[0].strftime('%d.%m.%Y') + ":\n"

            title = ' '.join(str(exam[1]).split())
            lecturer = ' '.join(str(exam[2]).split())
            classroom = ' '.join(str(exam[3]).split())

            message += title + ' | ' + lecturer + ' | ' + classroom + "\n"
            message += "------------\n"
        if len(message) == 0:
            message = 'Похоже расписания экзаменов для вашей группы нет в базе'

    except BaseException as e:
        message = "Случилось что то странное, попробуйте ввести команду заново"

    bot.send_message(cid, message, reply_markup=get_date_keyboard())


# text message handler
@bot.message_handler(func=lambda message: True, content_types=['text'])
def response_msg(m):
    cid = m.chat.id
    if m.text in ScheduleType:
        # Статистика
        if config['STATISTIC_TOKEN'] != '':
            track(config['STATISTIC_TOKEN'], m.chat.id, m.text, 'schedule')
        else:
            logger.info('message: {0}'.format(m.text))

        # По умолчанию week_type равен -1 и при таком значении будут выводится все занятия,
        # т.е и для чётных и для нечётных недель
        week_type = -1

        if m.text == "Вся неделя":
            days = ScheduleType[m.text]
        elif m.text == "Сегодня":
            today = datetime.now()
            # Если запрашивается расписание на сегодняшний день,
            # то week_type равен остатку от деления на 2 номера недели в году, т.е он определяет чётная она или нечётная
            week_type = (today.isocalendar()[1] + int(config["WEEK_TYPE"])) % 2

            # Если сегодня воскресенье, то показывается расписание на понедельник следующей недели
            # Также в этом случае, как week_type используется тип следующей недели
            if datetime.weekday(today) == 6:
                today += timedelta(days=1)
                week_type = (week_type + 1) % 2

            days = [daysOfWeek[datetime.weekday(today)]]
        elif m.text == 'Завтра':
            tomorrow = datetime.now()
            # Если запрашивается расписание на сегодняшний день,
            # то week_type равен остатку от деления на 2 номера недели в году, т.е он определяет чётная она или нечётная
            week_type = (tomorrow.isocalendar()[1] + int(config["WEEK_TYPE"])) % 2

            tomorrow += timedelta(days=1)
            # Если сегодня воскресенье, то показывается расписание на понедельник следующей недели
            # Также в этом случае, как week_type используется тип следующей недели
            if datetime.weekday(tomorrow) == 6:
                tomorrow += timedelta(days=1)
                week_type = (week_type + 1) % 2

            days = [daysOfWeek[datetime.weekday(tomorrow)]]
        else:
            days = [ScheduleType[m.text]]

        for day in days:
            try:
                with ScheduleDB(config) as db:
                    user = db.find_user(cid)
                if user and user[0] != "":
                    result = create_schedule_text(user[0], day, week_type)
                    for schedule in result:
                        bot.send_message(cid, schedule, reply_markup=get_date_keyboard())
                else:
                    bot.send_message(cid, "Вас ещё нет в базе данных, поэтому пройдите простую процедуру регистрации")
                    command_registration(m)
            except BaseException as e:
                logger.warning('response_msg: {0}'.format(str(e)))
                bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново")
    else:
        # Статистика
        if config['STATISTIC_TOKEN'] != '':
            track(config['STATISTIC_TOKEN'], m.chat.id, m.text, 'unknown')
        else:
            logger.info('unknown message: {0}'.format(m.text))

        bot.send_message(cid, "Неизвестная команда", reply_markup=get_date_keyboard())


# -------------------------------------
#  BOT CALLBACKS
# -------------------------------------


@bot.callback_query_handler(func=lambda call: "reg:stage 2:" in call.data)
def callback_registration(call):
    cid = call.message.chat.id

    # Парсинг сообщения указывающего стадию регистрации
    # reg : stage : tag
    callback_data = re.split(r':', call.data)

    # Процедура регистрации проходит в четрые этапа:
    # 1 этап: выбор учебного заведения
    # 2 этап: выбор факультета <--
    # 3 этап: выбор группы
    # 4 этап: добавление данных о принадлежности пользователя к учебному заведению в БД
    try:
        # Статистика
        if config['STATISTIC_TOKEN'] != '':
            track(config['STATISTIC_TOKEN'], cid, 'stage 2', 'registration-stage-2')

        keyboard = types.InlineKeyboardMarkup()

        organization_id = callback_data[2]

        with ScheduleDB(config) as db:
            result = db.get_faculty(organization_id)

        for row in result:
            callback_button = types.InlineKeyboardButton(
                text=str(row[0]),
                callback_data="reg:stage 3:{0}".format(
                    str(row[1])[:organization_field_length + faculty_field_length]))
            keyboard.add(callback_button)

        bot.send_message(cid, "Выберите факультет:", reply_markup=keyboard)
    except BaseException as e:
        logger.warning('Registration problem: {0}'.format(str(e)))
        bot.send_message(cid, "Случилось что-то странное, попробуйте начать сначала, введя команду /registration")


@bot.callback_query_handler(func=lambda call: "reg:stage 3:" in call.data)
def callback_registration(call):
    cid = call.message.chat.id

    # Парсинг сообщения указывающего стадию регистрации
    # reg : stage : tag
    callback_data = re.split(r':', call.data)

    # Процедура регистрации проходит в четрые этапа:
    # 1 этап: выбор учебного заведения
    # 2 этап: выбор факультета
    # 3 этап: выбор группы <--
    # 4 этап: добавление данных о принадлежности пользователя к учебному заведению в БД
    try:
        # Статистика
        if config['STATISTIC_TOKEN'] != '':
            track(config['STATISTIC_TOKEN'], cid, 'stage 3', 'registration-stage-3')

        keyboard = types.InlineKeyboardMarkup()

        faculty_id = callback_data[2]

        with ScheduleDB(config) as db:
            result = db.get_group(faculty_id)

        for row in result:
            callback_button = types.InlineKeyboardButton(
                text=str(row[0]),
                callback_data="reg:stage 4:{0}".format(str(row[1])))
            keyboard.add(callback_button)

        bot.send_message(cid, "Выберите группу:", reply_markup=keyboard)
    except BaseException as e:
        logger.warning('Registration problem: {0}'.format(str(e)))
        bot.send_message(cid, "Случилось что-то странное, попробуйте начать сначала, введя команду /registration")


@bot.callback_query_handler(func=lambda call: "reg:stage 4:" in call.data)
def callback_registration(call):
    cid = call.message.chat.id

    # Парсинг сообщения указывающего стадию регистрации
    # reg : stage : tag
    callback_data = re.split(r':', call.data)

    # Процедура регистрации проходит в четрые этапа:
    # 1 этап: выбор учебного заведения
    # 2 этап: выбор факультета
    # 3 этап: выбор группы
    # 4 этап: добавление данных о принадлежности пользователя к учебному заведению в БД <--
    try:
        # Статистика
        if config['STATISTIC_TOKEN'] != '':
            track(config['STATISTIC_TOKEN'], cid, 'stage 4', 'registration-stage-4')

        group_id = callback_data[2]

        with ScheduleDB(config) as db:
            row = db.get_group(group_id)
            user = db.find_user(cid)

        if user:
            db.update_user(cid, call.message.chat.first_name, call.message.chat.username, str(row[0][1]))
        else:
            db.add_user(cid, call.message.chat.first_name, call.message.chat.username, str(row[0][1]))

        bot.send_message(cid, "Отлично, вы зарегистрировались, ваша группа: " + row[0][0] +
                         "\nЕсли вы ошиблись, то просто введиде команду /registration и измените данные",
                         reply_markup=get_date_keyboard())
        bot.send_message(cid, "Теперь вы можете настроить автоматическую отправку расписания в заданное вами время,"
                              " введя команду /auto_posting_on <время>, "
                              "где <время> должно иметь формат ЧЧ:ММ")

    except BaseException as e:
        logger.warning('Registration problem: {0}'.format(str(e)))
        bot.send_message(cid, "Случилось что-то странное, попробуйте начать сначала, введя команду /registration")


@bot.callback_query_handler(func=lambda call: "ap:" in call.data)
def callback_auto_posting(call):
    cid = call.message.chat.id

    try:
        callback_data = re.split(r':', call.data)

        # Проверка на соответствие введённых пользователем данных принятому формату
        if len(callback_data) != 4:
            bot.send_message(cid,
                             "Вы отправили пустую строку или строку неправильного формата. Правильный формат ЧЧ:ММ",
                             reply_markup=get_date_keyboard())
            return

        hour = ''.join(filter(lambda x: x.isdigit(), callback_data[1]))
        minutes = ''.join(filter(lambda x: x.isdigit(), callback_data[2]))
        is_today = callback_data[3]

        # Проверка на соответствие введённых пользователем данных принятому формату
        if not hour.isdigit() or not minutes.isdigit():
            bot.send_message(cid,
                             "Вы отправили пустую строку или строку неправильного формата. Правильный формат ЧЧ:ММ",
                             reply_markup=get_date_keyboard())
            return

        with ScheduleDB(config) as db:
            if db.set_auto_post_time(cid, (hour + ":" + minutes + ":" + "00").rjust(8, '0'), is_today):
                bot.send_message(cid, "Время установлено", reply_markup=get_date_keyboard())
            else:
                bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново",
                                 reply_markup=get_date_keyboard())
    except BaseException as e:
        logger.warning('callback_auto_posting: {0}'.format(str(e)))
        bot.send_message(cid, "Случилось что то странное, попробуйте ввести команду заново")


# -------------------------------------
#  FLASK ROUTES
# -------------------------------------


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@app.route("/remove_webhook", methods=["GET", "HEAD"])
def remove_webhook():
    bot.remove_webhook()
    return "ok", 200


@app.route("/reset_webhook", methods=["GET", "HEAD"])
def reset_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH, certificate=open(config["WEBHOOK_SSL_CERT"], 'r'))
    return "ok", 200


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

if __name__ == '__main__':
    # Start flask server
    app.run(
        host=config["WEBHOOK_LISTEN"],
        port=config["WEBHOOK_PORT"],
        ssl_context=(config['WEBHOOK_SSL_CERT'], config['WEBHOOK_SSL_PRIV']),
        debug=True)
