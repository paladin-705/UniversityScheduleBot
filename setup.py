# -*- coding: utf-8 -*-
import sqlite3

try:
	con = sqlite3.connect('base/base.db')
	cur = con.cursor()
	cur.execute("CREATE TABLE users(id INT, name TEXT, username TEXT, hash TEXT);")
	cur.execute("CREATE TABLE schedule(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, tag TEXT, day TEXT, number INTEGER, type TEXT, startTime TEXT, endTime TEXT, title TEXT, classroom TEXT, lecturer TEXT);")
except sqlite3.Error:
	print("Oops! some errors")
finally:
	con.close()
