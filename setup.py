# -*- coding: utf-8 -*-
import os
import sqlite3

import config

try:
    os.makedirs('base')
    os.makedirs('log')
except OSError:
    pass

try:
    con = sqlite3.connect(config.db_path)
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
