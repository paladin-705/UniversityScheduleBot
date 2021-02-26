# -*- coding: utf-8 -*-
import configparser
import os

config_file = configparser.ConfigParser()
config = config_file['DEFAULT']

current_path = os.path.abspath(os.path.dirname(__file__))
config_file.read(current_path + '/' + "config.ini")
