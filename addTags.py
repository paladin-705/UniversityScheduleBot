# -*- coding: utf-8 -*-
import sqlite3
import hashlib

try:
    con = sqlite3.connect('base/base.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM organizations')
    result = cur.fetchall()
    
    for row in result:
        tag = hashlib.sha256((row[1] + row[2] + row[3]).encode('utf-8')).hexdigest()
        cur.execute('UPDATE organizations SET tag = (?) WHERE id = (?)',(tag, row[0]))
        print ('{0:6} | {1:25} | {2:10} | {3:10} | {4:64}'.format(str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4])))
    con.commit()
except sqlite3.Error:
    print("Oops! some errors")
finally:
    con.close()
