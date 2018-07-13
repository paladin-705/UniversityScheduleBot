UniversityScheduleBot
=========================
Бот для Telegram показывающий расписание занятий. Вы можете добавить его себе в Telegram, перейдя по ссылке: [@UniversityScheduleBot](http://telegram.me/UniversityScheduleBot)

Wiki проекта: [UniversityScheduleBot Wiki](https://github.com/paladin-705/UniversityScheduleBot/wiki)

![Build Status](https://travis-ci.org/paladin-705/UniversityScheduleBot.svg?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/dc51667700670e46bdf2/maintainability)](https://codeclimate.com/github/paladin-705/UniversityScheduleBot/maintainability)

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
    ├── auto_posting_thread.py
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
Установите вебхук:
Для этого откройте браузер и перейдите по адресу:
```shell
<WEBHOOK_HOST>:<WEBHOOK_PORT>/reset_webhook
```

### Windows:
То же самое, что и для Linux, но без терминала:
 1. Скачайте репозиторий
 2. Запустите setup.py
 3. Скопируйте свой токен, адрес сервера, пути к сертификатам и данные для подключения к PostgreSQL БД в файл config.ini
 4. Запустите setup_db.py
 5. Запустите UniversityScheduleBot.py
 6. Установите вебхук, открыв браузер и перейдя по адресу: <WEBHOOK_HOST>:<WEBHOOK_PORT>/reset_webhook

Включение автоматической отправки расписания
------------
Автоматическая отправка распсиания вынесена в отдельный файл auto_posting_thread.py. Для того, чтобы включить автоматическую отправку расписания нужно запустить этот файл:
```shell
python3 auto_posting_thread.py &
```

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

Добавление расписания и организаций в БД
------------
Для добавления расписания или организации в базу данных, необходимо отправить POST запрос, с данными в json формате. В начале необходимо добавить в базу организацию, чтобы пользователи могли выбрать её при регистрации, а после её добавления в БД, можно добавить расписание для этой организации.

### Общий вид запроса:

#### Параметры:
|Название параметра| Обязательный параметр | Описание |
:----------------| ------------- | -------------
| key | &#10003; | Ключ доступа к api, по умолчанию в качестве ключа используется токен бота |
| data | &#10003; | Массив содержащий в себе элементы которое нужно добавить в базу |

Пример запроса: 
```json
{
    "key": "ключ доступа к api",
    "data": [ ... ]
}
```

### Добавление организации в базу:
Необходимо отправить POST запрос по адресу:
```
<адрес сервера>/api/organization
```

#### Параметры:
|Название параметра| Обязательный параметр | Описание |
:----------------| ------------- | -------------
| organization | &#10003; | Название учебного заведения |
| group | &#10003; | Название группы |
| faculty |  | Название факультета |

#### Пример запроса:
```json
{
    "key": "ключ доступа к api",
    "data": [
        {
            "organization": "ВУЗ №1",
            "faculty": "Факультет  №1",
            "group": "Группа №1",

        },
        {
            "organization": "ВУЗ №2",
            "group": "Группа №2",

        },
        { ... },
        ...
        ]
}
```

#### Результат:
В ответ придут данные в json формате имеющие следюущую структуру:
```json
{
  "failed": [],
  "ok": []
}
```
Массив "failed" содержит организации которые не удалось добавить в БД, так как они уже были добавлены ранее (основная причина). В массиве "ok" содержатся организации которые были успешно добавлены в БД, также для каждой такой организации приходит её уникальный идентификатор "tag" для последующего добавления расписания этой организации.

#### Пример ответа:
```json
{
  "failed": [
    {
      "data": {
        "faculty": "Факультет №2", 
        "group": "Группа №2", 
        "organization": "ВУЗ №1"
      }, 
      "tag": null
    }, 
    { ... },
    ...
  ], 
  "ok": [
  	{
      "data": {
        "faculty": "Факультет №1", 
        "group": "Группа №1", 
        "organization": "ВУЗ №1"
      }, 
      "tag": "уникальный идентификатор организации"
    }, 
    { ... },
    ...
  	]
}
```

### Добавление расписания в базу:
Необходимо отправить POST запрос по адресу:
```
<адрес сервера>/api/schedule
```
Само расписание должно иметь вид отдельных занятий, которые добавляются в БД.

#### Параметры:
|Название параметра| Обязательный параметр | Описание |
:----------------| ------------- | -------------
| tag | &#10003; | Уникальный идентификатор организации, которой принадлежит расписание, его можно получить в ответе после добавления организации в БД |
| day | &#10003; | День, в который проходит занятие. Принимает значения: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday |
| number | &#10003; | Порядковый номер занятия. Целое неотрицательное число |
| week_type | &#10003; | Целое неотрицательное число. Принимает значение 0(по числителю) 1(по знаменателю) 2(каждую неделю) |
| title | &#10003; | Название занятия |
| classroom | &#10003; | Кабинет в котором проходит занятие |
| time_start | | Время начала занятия |
| time_end | | Время окончания занятия |
| lecturer | | ФИО Преподавателя |

#### Пример запроса:
```json
{
	"key": "key-test",
	"data": [
		{
			"tag": "c3e6dc0f7225b28e3b0c44298a68f2 ",
			"day": "Monday",
			"number": 1,
			"week_type": 0,
			"title": "Переворачивание пингвинов",
			"classroom": "Антарктида",
			"lecturer": "Пингвин",
			"time_start": "08:30",
			"time_end": "09:15",
		},
		{
			 "tag": "9937b02f18e3ca7043a71877484989 ",
			 "day": "Tuesday",
			 "number": 2,
			 "week_type": 1,
			 "title": "Информатика",
			 "classroom": "3-403"
		},
		{ ... },
		...
		]
}
```

#### Результат:
В ответ придут данные в json формате имеющие следюущую структуру:
```json
{
  "failed": []
}
```
Массив "failed" содержит занятия которые не удалось добавить в БД.

#### Пример ответа:
```json
{
	"failed": [
		{
			 "tag": "9937b02f18e3ca7043a71877484989 ",
			 "day": "Tuesday",
			 "number": 2,
			 "week_type": 1,
			 "title": "Информатика",
			 "classroom": "3-403"
		},
		{ ... },
		...
		]
}
```
