# -*- coding: utf-8 -*-
import configparser
import os
import psycopg2


def init_db(name, user, pasw, host, schema_path):
    with psycopg2.connect(dbname=name, user=user, password=pasw, host=host) as db:
        with open(schema_path, "r") as f:
            db.cursor().execute(f.read())
        db.commit()


if __name__ == "__main__":
    # Считывание конфигурационного файла или его создание с настройками по умолчанию
    config = configparser.ConfigParser()

    current_path = os.path.abspath(os.path.dirname(__file__))
    if os.path.exists(current_path + '/' + "config.ini"):
        config.read(current_path + '/' + "config.ini")
    else:
        config['DEFAULT'] = {'TOKEN': 'место для токена',
                             'PROXY_IP': '127.0.0.1',
                             'PROXY_PORT': '80',
                             'DB_NAME': 'название базы данных',
                             'DB_HOST': 'адрес БД',
                             'DB_USER': 'пользователь для работы с БД',
                             'DB_PASSWORD': 'пароль пользователя',
                             'LOG_DIR_PATH': current_path + '/' + 'log' + '/',
                             'WEEK_TYPE': 0,
                             'STATISTIC_TOKEN': ''
                             }
        with open(current_path + '/' + 'config.ini', 'w') as configfile:
            config.write(configfile)

    # Создание директорий
    try:
        os.makedirs(config["DEFAULT"]["LOG_DIR_PATH"])
    except OSError:
        pass

    # Настройка базы данных
    try:
        init_db(
            name=config["DEFAULT"]["DB_NAME"],
            user=config["DEFAULT"]["DB_USER"],
            pasw=config["DEFAULT"]["DB_PASSWORD"],
            host=config["DEFAULT"]["DB_HOST"],
            schema_path=current_path + "/" + "schema.sql")
    except BaseException as e:
        print(str(e))
