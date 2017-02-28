# -*- coding: utf-8 -*-
import sqlite3
import os

try:
    os.makedirs('base')
    os.makedirs('log')
except OSError:
    pass
	
try:
    con = sqlite3.connect('base/base.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, username TEXT, scheduleTag TEXT);")
    cur.execute("CREATE TABLE organizations(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, organization TEXT, faculty TEXT, studGroup TEXT, tag TEXT);")
    cur.execute("CREATE TABLE schedule(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, tag TEXT, day TEXT, number INTEGER, type TEXT, startTime TEXT, endTime TEXT, title TEXT, classroom TEXT, lecturer TEXT);")
    cur.execute("CREATE TABLE reports (report_id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,report TEXT);")
except:
    print("Oops! some errors")
finally:
    con.close()
