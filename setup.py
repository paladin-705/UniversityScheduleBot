# -*- coding: utf-8 -*-
import sqlite3

try:
	con = sqlite3.connect('base/base.db')
	cur = con.cursor()
	cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, username TEXT, scheduleTag TEXT);")
	cur.execute("CREATE TABLE organizations(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, organization TEXT, faculty TEXT, studGroup TEXT, tag TEXT);")
	cur.execute("CREATE TABLE schedule(tag TEXT PRIMARY KEY NOT NULL, day TEXT, number INTEGER, type TEXT, startTime TEXT, endTime TEXT, title TEXT, classroom TEXT, lecturer TEXT);")
except sqlite3.Error:
	print("Oops! some errors")
finally:
	con.close()
