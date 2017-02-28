UniversityScheduleBot
=========================
Бот для Telegram показывающий расписание занятий

Структура репозитория
------------
    .
    ├── config.py                         # Настройки бота
    ├── parser.py                         # Тестовый парсер расписания
    ├── scheduleCreator.py
    ├── setup.py                          # Скрипт для создания БД и директорий
    ├── UniversityScheduleBot.py 
    ├── .gitignore
    ├── testSchedule.xls                  # Расписание для parser.py
    ├── commandsList.txt                  # Лист команд для @BotFather
    ├── LICENSE
    └── README.md

Зависимости
------------
Данная программа требует для работы Python 3 и библиотеку xlrd (её наличие необходимо лишь для работы parser.py)

Установка
------------
###Linux:
Клонируйте репозиторий и запустите setup.py: 
```shell
git clone https://github.com/paladin-705/UniversityScheduleBot.git
cd UniversityScheduleBot
python3 setup.py
```
Скопируйте свой токен в файл config.py:
```python
token = '<место для токена>'
```
Запустите бота, введя: 
```shell
python3 UniversityScheduleBot.py &
```
###Windows:
То же самое, что и для Linux, но без терминала:
 1. Скачайте репозиторий
 2. Запустите setup.py
 3. Скопируйте свой токен в файл config.py
 4. Запустите UniversityScheduleBot.py

Парсинг расписания в БД
------------
С ботом поставляется парсер excel таблицы с расписанием (файл parser.py), созданный для расписания моего ВУЗа (КФ МГТУ им.Баумана), само расписание лежит в файле testSchedule.xls. Для других ВУЗов нужно будет создать свой парсер для записи расписания в БД. Данные в базе должны распологаться следующим образом:
```
Таблица organizations:
┌───┬──────────────┬───────────┬─────┐
│id │ organization │ studGroup │ tag │
├───┼──────────────┼───────────┼─────┤
Описание полей:
  id - автоинкрементируемое ключ таблицы
  organization - название ВУЗа
  studGroup - группа
  tag - хэш от конкатенации строк organization и studGroup, в данном случае sha256

Таблица schedule:
┌───┬─────┬─────┬────────┬──────┬───────────┬─────────┬───────┬───────────┬──────────┐
│id │ tag │ day │ number │ type │ startTime │ endTime │ title │ classroom │ lecturer │
├───┼─────┼─────┼────────┼──────┼───────────┼─────────┼───────┼───────────┼──────────┤
Описание полей:
  id - автоинкрементируемое ключ таблицы
  tag - указывает на принадлежность данной строки определённой группе, соответсвует полю tag из таблицы organization
  day - принимает значения: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
  number - порядковый номер занятия
  type - принимает значение 0(по числителю) 1(по знаменателю) 2(каждую неделю)
  startTime и endTime - время начала и конца занятия
  title - название
  classroom - кабинет
  lecturer - преподаватель
```
