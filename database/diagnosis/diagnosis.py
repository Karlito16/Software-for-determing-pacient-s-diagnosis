#!/usr/bin/python3
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as Et
# try:
#     from modules.my_xml import *
# except ModuleNotFoundError:
from database.diagnosis.modules.my_xml import *


class Diagnosis:
    """Klasa Diagnosis stvara objekt dijagnoze.
    Metode nad objektom dijagnoze su sljedeće:
        --> add (dodavanje dijagnoze i njenih simptoma)
        --> remove (uklanjanje dijagnoze)
        --> add_symptom (dodavanje simptoma)
        --> remove_symptom (uklanjanje simptoma)
        --> get_category (kategorija dijagnoze)
        --> set_category (postavljanje kategorije)"""

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.tree = Et.parse(path)
        self.root = self.tree.getroot()
        self.parents = self.get_parents()
        self.element = self.get_element()
        self.children = self.get_children()
        self.symptoms = self.get_symptoms()
        return

    def get_element_old(self, pos=0):
        try:
            element = self.root[pos]
        except IndexError:
            return None
        else:
            if element.attrib["name"] == self.name:
                return element
            # return self.get_element(pos + 1)  --> This line of code has an unknown error ? : fix this
            return self.get_element()

    def get_element(self):
        for parent in self.parents:
            if parent.attrib["name"] == self.name:
                return parent
        return None

    def get_parents(self):
        return self.tree.iter('diagnosis')

    def get_children(self):
        try:
            return list(self.element)
        except TypeError:  # case if self.element is None
            return None

    def get_symptoms_yeild(self):
        for element in self.children:
            yield element.text

    def get_symptoms(self):
        tmp_list = []
        if self.children is not None:
            for element in self.children:
                tmp_list.append(element.text)
            return tmp_list
        return None

    def update(self):
        self.tree.write(self.path, encoding='utf-8')
        pretty_print(self.path)

    def add(self, category):
        Et.SubElement(self.root, 'diagnosis', {"name": self.name, "category": category})
        self.parents = self.get_parents()
        self.element = self.get_element()
        return True

    def remove(self):
        self.root.remove(self.element)
        return True

    def add_symptom(self, symptom):
        child = Et.SubElement(self.element, 'symptom')
        child.text = symptom
        return True

    def remove_symptom(self, symptom):
        for element in self.element:
            if element.text == symptom:
                self.element.remove(element)
                return True
        return False

    def get_category(self):
        return self.element.attrib["category"]

    def set_category(self, category):
        self.element.set("category", category)
        return True

    def set_name(self, name):
        for parent in self.parents:
            if parent.attrib["name"] == name:
                return False
        self.element.set("name", name)
        return True
