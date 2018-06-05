UniversityScheduleBot
=========================
Бот для Telegram показывающий расписание занятий. Вы можете добавить его себе в Telegram, перейдя по ссылке: [@UniversityScheduleBot](http://telegram.me/UniversityScheduleBot)

Wiki проекта: [UniversityScheduleBot Wiki](https://github.com/paladin-705/UniversityScheduleBot/wiki)

![Build Status](https://travis-ci.org/paladin-705/UniversityScheduleBot.svg?branch=master)

Структура репозитория
------------
    .
    ├── config.py                         # Настройки бота
    ├── parser.py                         # Тестовый парсер расписания
    ├── scheduleCreator.py                # Функции для генерации сообщения с расписанием
    ├── scheduledb.py                     # Класс для работы с БД
    ├── setup.py                          # Скрипт для создания БД и директорий
    ├── UniversityScheduleBot.py 
    ├── .travis.yml
    ├── .gitignore  
    ├── schema.sql                        # Схема базы данных
    ├── testSchedule.xls                  # Расписание для parser.py
    ├── commandsList.txt                  # Лист команд для @BotFather
    ├── LICENSE
    └── README.md

Зависимости
------------
Данная программа требует для работы Python 3 и PostgreSQL.

Установка
------------
### Linux:
Клонируйте репозиторий: 
```shell
git clone https://github.com/paladin-705/UniversityScheduleBot.git
cd UniversityScheduleBot
pip install -r requirements.txt
```
Скопируйте свой токен бота и данные для подключения к PostgreSQL БД в файл setup.py (строки с 22 по 28):
```python
'TOKEN': 'место для токена',
'DB_NAME': 'название базы данных',
'DB_HOST': 'адрес БД',
'DB_USER': 'пользователь для работы с БД',
'DB_PASSWORD': 'пароль пользователя',
```
Запустите файл setup.py для начальной настройки бота:
```shell
python3 setup.py
```
Запустите бота, введя: 
```shell
python3 UniversityScheduleBot.py &
```
### Windows:
То же самое, что и для Linux, но без терминала:
 1. Скачайте репозиторий
 2. Скопируйте свой токен и данные для подключения к PostgreSQL БД в файл setup.py
 3. Запустите setup.py
 4. Запустите UniversityScheduleBot.py

Поддерживаемые команды
------------
|Команда| Описание команды|
:----------------| -------------
|/start|Выводит стартовое сообщение и предложение зарегистрироваться|
|/help|Выводит информацию о боте и список доступных команд|
|/registration|Выбор ВУЗа, факультета и группы для вывода расписания|
|/send_report \<сообщение\>|Можно отправить информацию об ошибке или что то ещё|
|/auto_posting_on \<время\>|Включение и выбор времени для автоматической отправки расписания в диалог, время должно иметь формат ЧЧ:ММ|
|/auto_posting_off|Выключение автоматической отправки расписания|

Парсинг расписания в БД
------------
С ботом поставляется парсер excel таблицы с расписанием (файл parser.py), созданный для расписания моего ВУЗа (КФ МГТУ им.Баумана), само расписание лежит в файле testSchedule.xls. Для других ВУЗов нужно будет создать свой парсер для записи расписания в БД. Данные в базе должны распологаться следующим образом:
```
Таблица organizations:
┌───┬──────────────┬───────────┬─────┐
│id │ organization │ studGroup │ tag │
├───┼──────────────┼───────────┼─────┤
Описание полей:
  id - автоинкрементируемый ключ таблицы
  organization - название ВУЗа
  studGroup - группа
  tag - для создания тега используется метод create_tag класса ScheduleDB

Таблица schedule:
┌───┬─────┬─────┬────────┬──────┬───────────┬─────────┬───────┬───────────┬──────────┐
│id │ tag │ day │ number │ type │ startTime │ endTime │ title │ classroom │ lecturer │
├───┼─────┼─────┼────────┼──────┼───────────┼─────────┼───────┼───────────┼──────────┤
Описание полей:
  id - автоинкрементируемый ключ таблицы
  tag - указывает на принадлежность данной строки определённой группе, соответсвует полю tag из таблицы organization
  day - принимает значения: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
  number - порядковый номер занятия
  type - принимает значение 0(по числителю) 1(по знаменателю) 2(каждую неделю)
  startTime и endTime - время начала и конца занятия
  title - название
  classroom - кабинет
  lecturer - преподаватель
```
