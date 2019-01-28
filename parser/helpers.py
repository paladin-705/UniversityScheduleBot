import re

daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

ScheduleType = {
    "Понедельник": daysOfWeek[0],
    "Вторник": daysOfWeek[1],
    "Среда": daysOfWeek[2],
    "Четверг": daysOfWeek[3],
    "Пятница": daysOfWeek[4],
    "Суббота": daysOfWeek[5],
    "Воскресенье": daysOfWeek[6],
    "Сегодня": "Today",
    "Завтра": "Tomorrow",
    "Вся неделя": daysOfWeek
}

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
        return ScheduleType[cell_value]
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
    result = re.split(r'(\w{1,2}\s?\d[_-]\d{3}|\d[_-]\d{3}|\w\.\d)', cell_value)
    if len(result) >= 3:
        return result[0]
    else:
        return ""


def parse_lecturer(cell_value):
    result = re.split(r'(\w{1,2}\s?\d[_-]\d{3}|\d[_-]\d{3}|\w\.\d)', cell_value)
    if len(result) >= 3:
        return result[len(result) - 1]
    else:
        return ""


def parse_classroom(cell_value):
    classroom = ""
    result = re.findall(r'\w{1,2}\s?\d[_-]\d{3}|\d[_-]\d{3}|\w\.\d', cell_value)
    if len(result) >= 1:
        # Кабинет
        for room in result:
            classroom += room + " "
    return classroom
