# -*- coding: utf-8 -*-
import re

import xlrd

import config
import scheduledb

romanDigit = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5,
    'VI': 6,
    'VII': 7,
    'VIII': 8,
    'IX': 9,
    'X': 10
}


def is_merged(sheet, row, column):
    try:
        for cell_range in sheet.merged_cells:
            row_low, row_high, column_low, column_high = cell_range
            if row in range(row_low, row_high) and column in range(column_low, column_high):
                return True
        return False
    except:
        return False


def parse_day(cell_value):
    if cell_value != "":
        return config.ScheduleType[cell_value]
    else:
        return ""


def parse_lesson_number(cell_value):
    result = re.findall(r'^\w{1,3}', cell_value)
    if len(result) == 1:
        return romanDigit[result[0]]
    else:
        return 0


def parse_time(cell_value):
    time_start = ""
    time_end = ""
    result = re.findall(r'\d{1,2}:\d{2}', cell_value)
    if len(result) == 2:
        time_start = result[0]
        time_end = result[1]
    return time_start, time_end


def parse_title(cell_value):
    result = re.split(r'(\w{1,2}\s?\d_\d{3}|\d_\d{3}|\w\.\d)', cell_value)
    if len(result) >= 3:
        return result[0]
    else:
        return ""


def parse_lecturer(cell_value):
    result = re.split(r'(\w{1,2}\s?\d_\d{3}|\d_\d{3}|\w\.\d)', cell_value)
    if len(result) >= 3:
        return result[len(result) - 1]
    else:
        return ""


def parse_classroom(cell_value):
    classroom = ""
    result = re.findall(r'\w{1,2}\s?\d_\d{3}|\d_\d{3}|\w\.\d', cell_value)
    if len(result) >= 1:
        # Кабинет
        for room in result:
            classroom += room + " "
    return classroom


if __name__ == "__main__":
    print("Enter file name: ")
    file_name = input()

    db = scheduledb.ScheduleDB()
    file = xlrd.open_workbook(file_name, formatting_info=True)

    organization = "МГТУ им.Баумана КФ"
    sheet_names = file.sheet_names()
    for index in range(file.nsheets):
        sheet = file.sheet_by_index(index)
        faculty = sheet_names[index]

        for col in range(2, sheet.ncols, 1):
            # Группа
            group = sheet.cell_value(0, col)
            print("{0}:".format(group))

            # Знаю что костыли костыльные но а что делать, надо как то выкручиваться
            if sheet.cell_value(1, col + 2) == "Понедельник":
                break
            if group == "":
                continue

            tag = db.add_organization(organization, faculty, group)
            if tag is None:
                print("Oops! some errors")
                continue

            day = ""
            for row in range(1, sheet.nrows, 2):
                number = parse_lesson_number(sheet.cell_value(row, 1))
                time_start, time_end = parse_time(sheet.cell_value(row, 1))
                title = parse_title(sheet.cell_value(row, col))
                classroom = parse_classroom(sheet.cell_value(row, col))
                lecturer = parse_lecturer(sheet.cell_value(row, col))

                if sheet.cell_value(row, 0) != "":
                    day = parse_day(sheet.cell_value(row, 0))
                print(day)

                if title is "":
                    continue

                if is_merged(sheet, row, col):
                    if db.add_lesson(tag, day, number, 2, time_start, time_end, title, classroom, lecturer):
                        print('{0:5}: {1:45} {2:20} | {3:5}-{4:5} | {5}'.format(
                            number, title, classroom, time_start, time_end, lecturer))
                else:
                    for count in range(0, 2, 1):
                        if (row + count) < sheet.nrows:
                            title = parse_title(sheet.cell_value(row + count, col))
                            classroom = parse_classroom(sheet.cell_value(row + count, col))
                            lecturer = parse_lecturer(sheet.cell_value(row + count, col))
                            if db.add_lesson(tag, day, number, 2, time_start, time_end, title, classroom, lecturer):
                                print('{0:5}: {1:45} {2:20} | {3:5}-{4:5} | {5}'.format(
                                    number, title, classroom, time_start, time_end, lecturer))
            print("\n")
        print("----------------------\n")
