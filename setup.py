# -*- coding: utf-8 -*-
import configparser
import os
import sqlite3

if __name__ == "__main__":
    # Считывание конфигурационного файла или его создание с настройками по умолчанию
    config = configparser.ConfigParser()
    if os.path.exists("config.ini"):
        config.read("config.ini")
    else:
        config['DEFAULT'] = {'token': '',
                             'db_path': 'base',
                             'log_dir_patch': 'log'}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    # Создание директорий
    try:
        os.makedirs(config["DEFAULT"]["db_path"])
        os.makedirs(config["DEFAULT"]["log_dir_patch"])
    except OSError:
        pass

    # Настройка базы данных
    try:
        con = sqlite3.connect(config["DEFAULT"]["db_path"] + "/" + "base.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE users( \
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                    name TEXT, username TEXT, \
                    scheduleTag TEXT, \
                    auto_posting_time TIME);")
        cur.execute("CREATE TABLE organizations(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                    organization TEXT, \
                    faculty TEXT, \
                    studGroup TEXT, \
                    tag TEXT);")
        cur.execute("CREATE TABLE schedule(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
                    tag TEXT, day TEXT, \
                    number INTEGER, \
                    type TEXT, \
                    startTime TEXT, \
                    endTime TEXT, \
                    title TEXT, \
                    classroom TEXT, \
                    lecturer TEXT);")
        cur.execute("CREATE TABLE reports (report_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    user_id INTEGER, \
                    report TEXT, \
                    date DATETIME);")
        con.close()
    except BaseException as e:
        print(str(e))
