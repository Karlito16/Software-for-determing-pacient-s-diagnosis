#!/usr/bin/python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as Et
import os
# try:
#     from modules.my_json import *
# except ModuleNotFoundError:
from database.user_info.modules.my_json import *


BASE_PATH = os.path.dirname(os.path.realpath(__file__))


class XmlFile:

    def __init__(self, path):
        self.path = path
        self.tree = Et.parse(path)
        self.root = self.tree.getroot()
        return


class NewUser:

    def __init__(self, user_info):
        self.user_info = user_info
        self.name = self.user_info['Ime']
        self.surname = self.user_info['Prezime']
        self.path = ''

    def create_folder(self):
        name = '{} {}'.format(self.name.capitalize(), self.surname.capitalize())
        try:
            path = '{}\\users\\{}'.format(BASE_PATH, name)
            os.mkdir(path)
        except FileExistsError:
            return False
        else:
            self.path = path
            return True

    def create_file(self):  # fix encoding issue! -- fixed!
        json_file = JsonFile('{}\\{}_{}.json'.format(self.path, self.name.lower(), self.surname.lower()))
        json_file.set_data(self.user_info)
        json_file.write()

