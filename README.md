UniversityScheduleBot
=========================
Бот для Telegram показывающий расписание занятий. Вы можете добавить его себе в Telegram, перейдя по ссылке: [@UniversityScheduleBot](http://telegram.me/UniversityScheduleBot)

Проект разделён на модули. Такая структура, позволяет устанавливать лишь необходимые разработчику части проекта. Ниже представлен список основных модулей бота:
* Модуль Telegram бота: [UniversityScheduleBot](./bot) - Бот для Telegram показывающий расписание занятий. Основной модуль проекта, осуществляющий обработку пользовательских запросов и формирование ответов на них.  
* Модуль для автоматической отправки расписания: [autoposting](./autoposting)
* Модуль для работы с базой данных бота (добавление/изменение/удаление групп и файлов расписания): [api_server](https://github.com/paladin-705/VkScheduleBot/tree/main/api_server)

Также бот совместим с ботом для ВК ([VkScheduleBot](https://github.com/paladin-705/VkScheduleBot)) - боты могут использовать одну базу данных для хранения расписания и информации о пользователях.

Wiki проекта: [UniversityScheduleBot Wiki](https://github.com/paladin-705/UniversityScheduleBot/wiki)

Готовые Docker образы
------------
Для всех модулей проекта уже собраны готовые Docker образы. 


### Модуль Telegram бота
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/paladin705/telegram_schedule_bot)

Docker Hub: [paladin705/telegram_schedule_bot](https://hub.docker.com/r/paladin705/telegram_schedule_bot)

### Модуль для автоматической отправки расписания
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/paladin705/telegram_schedule_bot_autoposting)

Docker Hub: [paladin705/telegram_schedule_bot_autoposting](https://hub.docker.com/r/paladin705/telegram_schedule_bot_autoposting)

### Модуль для работы с базой данных бота
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/paladin705/vk_schedule_bot_api)

Docker Hub: [paladin705/vk_schedule_bot_api](https://hub.docker.com/r/paladin705/vk_schedule_bot_api)

Структура репозитория
------------
    .
    ├── autoposting                       # Модуль для автоматической отправки расписания
    │   ├── auto_posting_thread.py            # Основной скрипт модуля
    │   ├── scheduleCreator.py                # Функции для генерации сообщения с расписанием
    │   ├── scheduledb.py                     # Класс для работы с БД
    │   ├── statistic.py                      # Отправка статистики на chatbase.com (На данный момент не используется - Chatbase прекращает работу 27 сентября 2021 года)
    │   ├── helpers.py                        # Вспомогательные функции
    │   ├── config.py                         # Настройки модуля 
    │   ├── requirements.txt                  # Список используемых библиотек
    │   ├── deploy                            # Скрипт для запуска Docker контейнера 
    │   ├── Dockerfile
    │   └── README.md
    ├── bot                               # Модуль бота для Telegram
    │   ├── UniversityScheduleBot.py          # Основной скрипт модуля
    │   ├── scheduleCreator.py                # Функции для генерации сообщения с расписанием
    │   ├── scheduledb.py                     # Класс для работы с БД
    │   ├── statistic.py                      # Отправка статистики на chatbase.com (На данный момент не используется - Chatbase прекращает работу 27 сентября 2021 года)
    │   ├── helpers.py                        # Вспомогательные функции
    │   ├── config.py                         # Настройки модуля 
    │   ├── requirements.txt                  # Список используемых библиотек
    │   ├── deploy                            # Скрипт для запуска Docker контейнера 
    │   ├── Dockerfile
    │   ├── commandsList.txt                  # Лист команд для @BotFather
    │   └── README.md
    ├── db                                # Файлы для базы данных
    │   └── schema.sql                        # Схема базы данных
    ├── docs                              # Файлы Wiki проекта
    │   └── gifs                              # Gif'ки с примерами использования команд
    │       ├── auto_posting_off_instruction.gif
    │       ├── auto_posting_on_instruction.gif
    │       ├── get_schedule_instruction.gif
    │       ├── registration_instruction.gif
    │       └── send_report_instruction.gif
    ├── .gitignore  
    ├── LICENSE
    └── README.md
