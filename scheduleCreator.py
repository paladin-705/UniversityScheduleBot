# -*- coding: utf-8 -*-
import sqlite3

import config


def print_type(raw_type, week_type=-1):
    # Если задан тип недели (числитель/знаменатель), т.е week_type не равен значению по умолчанию, 
    # то дополнительная информация о типе недели не выводится
    if week_type != -1:
        return ""

    raw_type = int(raw_type)
    if raw_type == 0:
        return "числ"
    elif raw_type == 1:
        return "знам"
    elif raw_type == 2:
        return ""


def get_schedule_raw(tag, day, week_type):
    data = []
    try:
        con = sqlite3.connect(config.db_path)
        cur = con.cursor()
        if week_type != -1:
            cur.execute('SELECT number,title,classroom,type FROM schedule \
                        WHERE tag = (?) AND day = (?) AND (type = 2 OR type = ?) \
                        ORDER BY number, type ASC', [tag, day, week_type])
        else:
            cur.execute('SELECT number,title,classroom,type FROM schedule \
                        WHERE tag = (?) AND day = (?) ORDER BY number, type ASC', [tag, day])
        data = cur.fetchall()
        con.close()
    except:
        print('DB error')
        raise Exception('DB error')
    finally:
        return data


def create_schedule_text(tag, day, week_type=-1):
    result = []
    schedule = ""
    try:
        data = get_schedule_raw(tag, day, week_type)

        schedule += ">{0}:\n".format(config.daysOfWeek_rus[day])
        index = 0
        while index < len(data):
            row = data[index]

            schedule += str(row[0]) + " пара:\n"
            # Этот блок нужен для вывода тех занятий, где занятия по числителю и знамнателю различаются
            if index != len(data) - 1:
                # Сравнивается порядковый номер занятия данной и следующей строки и если они равны,
                # то они выводятся вместе
                if data[index + 1][0] == row[0]:
                    schedule += '{0} {1} {2}\n'.format(str(row[1]), str(row[2]), print_type(row[3], week_type))
                    index += 1
                    row = data[index]
                    schedule += '{0} {1} {2}\n'.format(str(row[1]), str(row[2]), print_type(row[3], week_type))
                else:
                    schedule += '{0} {1} {2}\n'.format(str(row[1]), str(row[2]), print_type(row[3], week_type))
            else:
                schedule += '{0} {1} {2}\n'.format(str(row[1]), str(row[2]), print_type(row[3], week_type))

            schedule += "------------\n"
            index += 1
        result.append(schedule)
    except:
        print("Some errors")
    finally:
        return result


def create_schedule_xls(tag, day):
    print("foobar")


def create_schedule_pdf(tag, day):
    print("foobar")
