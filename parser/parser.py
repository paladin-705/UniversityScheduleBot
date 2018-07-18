# -*- coding: utf-8 -*-
from helpers import *
from api import add_organization, add_lesson
import xlrd


if __name__ == "__main__":
    print("Enter file name: ")
    file_name = input()

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

            tag = add_organization(organization, faculty, group)
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

                if title is "" or title.isspace():
                    continue

                if is_merged(sheet, row, col):
                    if add_lesson(tag, day, number, 2, time_start, time_end, title, classroom, lecturer):
                        print('{0:5}: {1:60} | {2:20} | {3:5}-{4:5} | {5}'.format(
                            number, title, classroom, time_start, time_end, lecturer))
                else:
                    for count in range(0, 2, 1):
                        if (row + count) < sheet.nrows:
                            title = parse_title(sheet.cell_value(row + count, col))
                            if title is "" or title.isspace():
                                continue

                            classroom = parse_classroom(sheet.cell_value(row + count, col))
                            lecturer = parse_lecturer(sheet.cell_value(row + count, col))
                            if add_lesson(tag, day, number, count, time_start, time_end, title, classroom, lecturer):
                                print('{0:5}: {1:60} | {2:20} | {3:5}-{4:5} | {5}'.format(
                                    number, title, classroom, time_start, time_end, lecturer))
            print("\n")
        print("----------------------\n")
