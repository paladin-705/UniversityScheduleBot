# -*- coding: utf-8 -*-
import configparser

config_file = configparser.ConfigParser()
config = config_file['DEFAULT']

config_file.read('config.ini')
