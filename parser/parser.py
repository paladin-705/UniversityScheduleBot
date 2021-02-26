# -*- coding: utf-8 -*-
import xlrd
import xlwt
from api import add_organization, add_lesson
from xlutils.copy import copy as xlcopy

if __name__ == "__main__":
    print("Enter file name: ")
    file_name = input()

    file = xlrd.open_workbook(file_name, formatting_info=True)
    write_book = xlcopy(file)   # Excel книга в которой будет показано какие записи были добавлены в БД

    xlwt.add_palette_colour("ok_colour", 0x21)
    write_book.set_colour_RGB(0x21, 39, 91, 39)

    xlwt.add_palette_colour("fail_colour", 0x22)
    write_book.set_colour_RGB(0x22, 91, 39, 39)

    style_ok = xlwt.easyxf('pattern: pattern solid, fore_colour ok_colour')
    style_fail = xlwt.easyxf('pattern: pattern solid, fore_colour fail_colour')

    organization = "МГТУ им.Баумана КФ"
    sheet_names = file.sheet_names()
    for index in range(file.nsheets):
        sheet = file.sheet_by_index(index)
        write_sheet = write_book.get_sheet(index)

        faculty = sheet_names[index]

        for col in range(2, sheet.ncols, 1):
            # Группа
            group = sheet.cell_value(0, col)
            print("{0}:".format(group))

            # Знаю что костыли костыльные но а что делать, надо как то выкручиваться
            if sheet.cell_value(1, col + 1) == "Понедельник":
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

                        write_sheet.write(
                            row,
                            col,
                            sheet.cell_value(row, col),
                            style_ok
                        )
                    else:
                        print('{0:5}: {1:60} | {2:20} | {3:5}-{4:5} | {5} - FAILED'.format(
                            number, title, classroom, time_start, time_end, lecturer))

                        write_sheet.write(
                            row,
                            col,
                            sheet.cell_value(row, col),
                            style_fail
                        )
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
                                write_sheet.write(
                                    row + count,
                                    col,
                                    sheet.cell_value(row + count, col),
                                    style_ok
                                )
                            else:
                                print('{0:5}: {1:60} | {2:20} | {3:5}-{4:5} | {5} - FAILED'.format(
                                    number, title, classroom, time_start, time_end, lecturer))

                                write_sheet.write(
                                    row + count,
                                    col,
                                    sheet.cell_value(row + count, col),
                                    style_fail
                                )
            print("\n")
        print("----------------------\n")

    write_book.save('schedule.xls')  # Сохраняем таблицу
