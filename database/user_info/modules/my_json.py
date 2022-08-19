# !/usr/bin/python3
# -*- coding: utf-8 -*-


import json


class JsonFile:

    def __init__(self, file_path):
        self.path = file_path
        self.data = ''

    def set_data(self, data):
        self.data = data

    def get_data(self):
        file = open(self.path, 'r', encoding='utf-8')
        self.data = json.load(file)

    def write(self):
        """Metoda upisuje podatke iz 'data' u datoteku"""

        with open(self.path, 'w', encoding='utf-8') as write_file:
            json.dump(self.data, write_file, indent=4, ensure_ascii=False)
            write_file.close()
