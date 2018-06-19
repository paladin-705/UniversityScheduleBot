# -*- coding: utf-8 -*-
import configparser
import os


if __name__ == "__main__":
    # Считывание конфигурационного файла или его создание с настройками по умолчанию
    config = configparser.ConfigParser()

    current_path = os.path.abspath(os.path.dirname(__file__))
    if os.path.exists(current_path + '/' + "config.ini"):
        config.read(current_path + '/' + "config.ini")
    else:
        config['DEFAULT'] = {'TOKEN': 'место для токена',
                             'WEBHOOK_HOST': '',
                             'WEBHOOK_PORT': '',
                             'WEBHOOK_LISTEN': '0.0.0.0',
                             'WEBHOOK_SSL_CERT': '',
                             'WEBHOOK_SSL_PRIV': '',
                             'DB_NAME': 'название базы данных',
                             'DB_HOST': 'адрес БД',
                             'DB_USER': 'пользователь для работы с БД',
                             'DB_PASSWORD': 'пароль пользователя',
                             'LOG_DIR_PATH': current_path + '/' + 'log' + '/',
                             'WEEK_TYPE': '0',
                             'STATISTIC_TOKEN': ''
                             }
        with open(current_path + '/' + 'config.ini', 'w') as configfile:
            config.write(configfile)

    # Создание директорий
    try:
        os.makedirs(config["DEFAULT"]["LOG_DIR_PATH"])
    except OSError:
        pass
