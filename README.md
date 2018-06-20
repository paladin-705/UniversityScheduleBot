UniversityScheduleBot
=========================
Бот для Telegram показывающий расписание занятий. Вы можете добавить его себе в Telegram, перейдя по ссылке: [@UniversityScheduleBot](http://telegram.me/UniversityScheduleBot)

Wiki проекта: [UniversityScheduleBot Wiki](https://github.com/paladin-705/UniversityScheduleBot/wiki)

![Build Status](https://travis-ci.org/paladin-705/UniversityScheduleBot.svg?branch=master)

Структура репозитория
------------
    .
    ├── parser                            # Тестовый парсер расписания
    │   ├── parser.py
    │   └── testSchedule.xls
    ├── tests                             # Юнит-тесты для бота
    │   ├── test_scheduleCreator.py
    │   └── test_scheduledb.py
    ├── config.py                         # Настройки бота                     
    ├── statistic.py                      # Отправка статистики на chatbase.com
    ├── scheduleCreator.py                # Функции для генерации сообщения с расписанием
    ├── scheduledb.py                     # Класс для работы с БД
    ├── setup.py                          # Скрипт для создания файла настроек и директорий
    ├── setup_db.py                       # Скрипт для настройки БД
    ├── UniversityScheduleBot.py 
    ├── .travis.yml
    ├── .gitignore  
    ├── schema.sql                        # Схема базы данных
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

Создайте SSL сертификаты:
```shell
openssl genrsa -out webhook_pkey.pem 2048
openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
```
При вводе пункта Common Name, нужно написать IP адрес сервера, на котором будет запущен бот.
После завершения создания сертификата, появится два файла: webhook_pkey.pem и webhook_cert.pem.

Запустите файл setup.py для начальной настройки бота:
```shell
python3 setup.py
```

Скопируйте свой токен бота, адрес сервера, пути к сертификатам и данные для подключения к PostgreSQL БД в файл config.ini:
```python
TOKEN = 'место для токена'

WEBHOOK_HOST = 'IP адрес сервера, на котором будет запущен бот'
WEBHOOK_PORT = 'Порт на котором будет запущен бот. Список допустмиых портов: 443, 80, 88 и 8443'
WEBHOOK_SSL_CERT = 'Путь до webhook_cert.pem включая имя файла'
WEBHOOK_SSL_PRIV = 'Путь до webhook_pkey.pem включая имя файла'
                             
DB_NAME = 'название базы данных'
DB_HOST = 'адрес БД'
DB_USER = 'пользователь для работы с БД'
DB_PASSWORD = 'пароль пользователя'
```
Запустите файл setup_db.py для начальной настройки базы данных:
```shell
python3 setup_db.py
```
Запустите бота, введя: 
```shell
python3 UniversityScheduleBot.py &
```
### Windows:
То же самое, что и для Linux, но без терминала:
 1. Скачайте репозиторий
 2. Запустите setup.py
 3. Скопируйте свой токен, адрес сервера, пути к сертификатам и данные для подключения к PostgreSQL БД в файл config.ini
 4. Запустите setup_db.py
 4. Запустите UniversityScheduleBot.py

Настройка сбора статистики
------------
Для того, чтобы подключить свой аккаунт на Сhatbase для сбора статистики, просто введите свой ключ в файл config.ini:
```python
STATISTIC_TOKEN = 'место для ключа'
```

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
