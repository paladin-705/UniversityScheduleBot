# -*- coding: utf-8 -*-
from functools import lru_cache

import scheduledb
from config import config
from helpers import daysOfWeek_rus


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


@lru_cache(maxsize=128)
def create_schedule_text(tag, day, week_type=-1):
    result = []
    schedule = ""
    try:
        with scheduledb.ScheduleDB(config) as db:
            data = db.get_schedule(tag, day, week_type)

        schedule += ">{0}:\n".format(daysOfWeek_rus[day])
        index = 0
        while index < len(data):
            row = data[index]

            title = ' '.join(str(row[1]).split())
            classroom = ' '.join(str(row[2]).split())

            schedule += str(row[0]) + " пара:\n"
            # Этот блок нужен для вывода тех занятий, где занятия по числителю и знамнателю различаются
            if index != len(data) - 1:
                # Сравнивается порядковый номер занятия данной и следующей строки и если они равны,
                # то они выводятся вместе
                if data[index + 1][0] == row[0]:
                    schedule += '{0} {1} {2}\n'.format(title, classroom, print_type(row[3], week_type))

                    index += 1
                    row = data[index]
                    title = ' '.join(str(row[1]).split())
                    classroom = ' '.join(str(row[2]).split())

                    schedule += '{0} {1} {2}\n'.format(title, classroom, print_type(row[3], week_type))
                else:
                    schedule += '{0} {1} {2}\n'.format(title, classroom, print_type(row[3], week_type))
            else:
                schedule += '{0} {1} {2}\n'.format(title, classroom, print_type(row[3], week_type))

            schedule += "------------\n"
            index += 1
        result.append(schedule)
    except:
        pass
    finally:
        return result


def create_schedule_xls(tag, day):
    pass


def create_schedule_pdf(tag, day):
    pass
