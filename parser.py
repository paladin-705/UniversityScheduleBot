# -*- coding: utf-8 -*-
import xlrd
import re
import config

import sqlite3
import hashlib

romanDigit = {
        'I':1,
        'II':2,
        'III':3,
        'IV':4,
        'V':5,
        'VI':6,
        'VII':7,
        'VIII':8,
        'IX':9,
        'X':10
        }

def is_merged(row, column):
    try:
        for cell_range in sheet.merged_cells:
            row_low, row_high, column_low, column_high = cell_range
            if row in range(row_low, row_high) and column in range(column_low, column_high):
                #return (True, row_high-1)
                return True
        return False
    except:
        print("WOW! Such errors")
        return False

def addToDb(tag, day, number, rType, timeStart, timeEnd, cell_value):
    title = ""
    lector = ""
    classroom = ""
    
    try:
        #Название
        result = re.split(r'(\w{1,2}\s{0,1}\d_\d{3}|\d_\d{3}|\w\.\d)', cell_value)
        if len(result) >= 3:
                title = result[0]
                lector = result[len(result) - 1]
                            
        #Кабинет
        result = re.findall(r'\w{1,2}\s{0,1}\d_\d{3}|\d_\d{3}|\w\.\d', cell_value)
        if len(result) >= 1:
            #Кабинет
            for room in result:
                classroom += room + " "
            
        if title != "":
            
            con = sqlite3.connect('base/base.db')
            cur = con.cursor()
            cur.execute("INSERT INTO schedule(tag, day, number, type, startTime, endTime, title, classroom, lecturer) VALUES(?,?,?,?,?,?,?,?,?);",(tag, day, number, rType, timeStart, timeEnd, title, classroom, lector))
            con.commit()
            con.close()
            print ('{0:5}: {1:45} {2:20} | {3:5}-{4:5} | {5}'.format(number, title, classroom, timeStart, timeEnd, lector))
    except:
            print("Error: add to db")
            
print("Enter file name: ")
fileName = input()

file = xlrd.open_workbook(fileName,formatting_info=True)

organization = "МГТУ им.Баумана КФ"
sheet_names = file.sheet_names()
for index in range(file.nsheets):
    sheet = file.sheet_by_index(index)
    faculty = sheet_names[index]

    for col in range(2, sheet.ncols, 1):
        #Группа
        group = sheet.cell_value(0, col)
        print("{0}:".format(group))
        
        tag = hashlib.sha256((organization  + faculty + group).encode('utf-8')).hexdigest()

        #Знаю что костыли костыльные но а что делать, надо как то выкрычиваться
        if(sheet.cell_value(1, col+2) == "Понедельник"):
            break
        if(group == ""):
            continue
        
        try:
            con = sqlite3.connect('base/base.db')
            cur = con.cursor()
            cur.execute("INSERT INTO organizations(organization, faculty, studGroup, tag) VALUES(?,?,?,?);",(organization, faculty, group, tag))
            con.commit()
            con.close()
        except sqlite3.Error:
            print("Oops! some errors")
                    
        day = ""
            
        for row in range(1, sheet.nrows, 2):
            number = 0
            timeStart = ""
            timeEnd = ""

            #День
            if (sheet.cell_value(row, 0) != ""):
                    day = config.ScheduleType[sheet.cell_value(row, 0)]
                    print(day)

            #Номер пары
            result = re.findall(r'^\w{1,3}', sheet.cell_value(row, 1))
            if len(result) == 1:
                    number = romanDigit[result[0]]
                            
            #Время пары
            result = re.findall(r'\d{1,2}:\d{2}', sheet.cell_value(row, 1))
            if len(result) == 2:
                    timeStart = result[0]
                    timeEnd = result[1]

            if is_merged(row, col):
                addToDb(tag, day, number, 2, timeStart, timeEnd, sheet.cell_value(row, col))
            else:
                for count in range(0, 2, 1):
                    if(row + count) < sheet.nrows:
                        addToDb(tag, day, number, count, timeStart, timeEnd, sheet.cell_value(row + count, col))
        print ("\n")
    print ("----------------------\n")
