# UniversityScheduleBot autoposting script
Модуль выполняющий автоматическую рассылку расписания для [UniversityScheduleBot](../bot).

![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/paladin705/telegram_schedule_bot_autoposting)

Docker Hub: [paladin705/telegram_schedule_bot_autoposting](https://hub.docker.com/r/paladin705/telegram_schedule_bot_autoposting)

## Зависимости
Модуль использует Telegram Bot API для отправки расписания и СУБД PostgreSQL для хранения данных.


## Docker
Для запуска docker контейнера загружаемого с [Docker Hub](https://hub.docker.com/r/paladin705/telegram_schedule_bot_autoposting) можно использовать следующую команду:
```shell
docker run \
    -v ./autoposting/log:/app/log \
    -e DB_NAME=<Введите значение параметра> \
    -e DB_USER=Введите значение параметра<> \
    -e DB_PASSWORD=<Введите значение параметра> \
    -e DB_HOST=<Введите значение параметра> \
    -e TELEGRAM_API_TOKEN=<Введите значение параметра> \
    -e STATISTIC_TOKEN=<Введите значение параметра> \
    -e WEEK_TYPE=<Введите значение параметра> \
    -e TZ=<Введите значение параметра> \
    paladin705/telegram_schedule_bot_autoposting:latest
```

### Файлы
* `/app/log` - Директория где располагаются логи модуля

### Переменные среды

* `DB_NAME` - Название базы данных (БД) PostgreSQL
* `DB_USER` - Имя пользователя БД
* `DB_PASSWORD` - Пароль пользователя БД
* `DB_HOST` - Адрес БД
* `TELEGRAM_API_TOKEN` - Токен Telegram Bot API
* `STATISTIC_TOKEN` - Токен для отправки статистики на [chatbase.com](https://chatbase.com/). Необязательный параметр (На данный момент не используется - Chatbase прекращает работу 27 сентября 2021 года)
* `WEEK_TYPE` - Тип первой недели семестра 0 - числитель, 1 - знаменатель
* `TZ` - Часовой пояс. По умолчанию `Europe/Moscow`
