# -*- coding: utf-8 -*-
import sqlite3
import config

def printType(rawType):
    rawType = int(rawType)
    if rawType == 0:
        return "числ"
    elif rawType == 1:
        return "знам"
    elif rawType == 2:
        return ""

def getSchedule_raw(tag, day):
    data=[]
    try:
        con = sqlite3.connect('base/base.db')
        cur = con.cursor()
        cur.execute('SELECT number,title,classroom,type FROM schedule WHERE tag = (?) AND day = (?) ORDER BY number, type ASC',[tag, day])
        data = cur.fetchall()
    except:
        print('DB error')
        raise Exception ('DB error')
    finally:
        con.close()
        return data
    
def createSchedule_text(tag, day):
    result = []
    schedule = ""
    try:
        data = getSchedule_raw(tag, day)

        schedule += ">{0}:\n".format(config.daysOfWeek_rus[day])
        index=0
        while index < len(data):
            row = data[index]
            
            schedule += str(row[0]) + " пара:\n"
            if(index != len(data) - 1):
                if data[index + 1][0] == row[0]:
                    schedule += '{0:20} {1:10} {2}\n'.format(str(row[1]), str(row[2]), printType(row[3]))
                    index+=1
                    row = data[index]
                    schedule += '{0:20} {1:10} {2}\n'.format(str(row[1]), str(row[2]), printType(row[3]))
                else:
                    schedule += '{0:20} {1:10} {2}\n'.format(str(row[1]), str(row[2]), printType(row[3]))
            else:
                schedule += '{0:20} {1:10} {2}\n'.format(str(row[1]), str(row[2]), printType(row[3]))

            schedule += "------------\n"
            index+=1
        result.append(schedule)
    except:
        print("Some errors")
    finally:
        return result

def createSchedule_xls(tag, day):
    print("foobar")
    
def createSchedule_pdf(tag, day):
    print("foobar")
