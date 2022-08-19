#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Program za dodavanje dijagnoza i odgovarajućih simptoma u xml

import os
try:
    from database.diagnosis.diagnosis import *
except:
    from diagnosis import *


BASE_PATH = os.path.dirname(os.path.realpath(__file__))
XML_PATH = '{}\\diagnosis.xml'.format(BASE_PATH)
OPTIONS = ['dodavanje dijagnoze i njenih simptoma', 'uklanjanje dijagnoze', 'ime dijagnoze', 'dodavanje simptoma',
           'uklanjanje simptoma', 'kategorija dijagnoze', 'promjena kategorije', 'simptomi dijagnoze', 'promjena imena',
           'pregled datoteke', 'učini kopiju datoteke', 'popravi datoteku']
CONTINUE_OPTIONS = ['Za nastavak pritisni enter.', 'Za novu dijagnozu unesi "Da".', 'Za kraj unesi "Kraj".']


def print_menu(s=0, n=len(OPTIONS)):
    funcs = list()
    menu = '\n Ključ |{0}Opcija{0}\n{1}\n'.format(23 * ' ', 60 * '=')
    for i in range(s, n):
        option = OPTIONS[i]
        menu += '{0}{1}{0}|{2}{3}{2}\n'.format(((7 - len(str(i))) // 2) * ' ',
                                               i - s,
                                               ((54 - len(option)) // 2) * ' ',
                                               option)
        menu += '{}\n'.format(60 * '-')
        funcs.append(FUNCS[i])
    print(menu)
    return funcs


def print_continue_menu(s=0, n=len(CONTINUE_OPTIONS)):
    print()
    answers = ['', 'da', 'kraj']
    for i in range(s, n):
        print(CONTINUE_OPTIONS[i])
    return answers[s:n]


def on_add_diagnosis():
    category = input("Unesi kategoriju: ")
    symptoms = symptom_input()
    diagnosis.add(category)
    # return  # fix this!
    for symptom in symptoms:
        diagnosis.add_symptom(symptom)
    # diagnosis.update()
    print("Nova dijagnoza uspješno dodana! ({})".format(diagnosis.name))


def on_remove_diagnosis():
    diagnosis.remove()


def on_diagnosis_name():
    print('Ime trenutno odabrane dijagnoze: {}'.format(diagnosis.name))


def symptom_input(status=True, symptoms=[]):
    if status:
        print("Za prekid unosa pritisni enter.")
    symptom = input("Unesi simptom: ")
    if not symptom == '':
        symptoms.append(symptom)
        return symptom_input(False, symptoms)
    return symptoms


def on_add_symptom():
    symptoms = symptom_input()
    for symptom in symptoms:
        diagnosis.add_symptom(symptom)


def on_remove_symptom():
    symptoms = symptom_input()
    for symptom in symptoms:
        diagnosis.remove_symptom(symptom)


def on_get_category():
    print("\nKategorija trenutno odabrane dijagnoze ({}): {}".format(diagnosis.name, diagnosis.get_category()))


def on_set_category():
    category = input("Unesi kategoriju: ")
    diagnosis.set_category(category)


def on_get_symptoms():
    print()
    output = 'Simptomi dijagnoze: {}\n'.format(diagnosis.name)
    symptoms = diagnosis.get_symptoms()
    for symptom in symptoms:
        output += '--> {}\n'.format(symptom)
    print(output)


def on_set_name():
    name = input("Unesi novo ime: ")
    diagnosis.set_name(name)


def preview():
    diagnosis.update()
    output = '\nPregled datoteke: {}\n\n{}'.format(diagnosis.path, open(XML_PATH, 'r', encoding='UTF-8').read())
    print(output)


def file_backup():
    folder_path = '{}\\backup'.format(os.path.dirname(diagnosis.path))
    try:
        g = open('{}\\diagnosis_backup.xml'.format(folder_path), 'w')
    except FileNotFoundError:
        os.makedirs(folder_path)
        g = open('{}\\diagnosis_backup.xml'.format(folder_path), 'w')
    g.write(open(diagnosis.path, 'r').read())
    g.close()


def file_fix():
    f = open(XML_PATH, 'w')
    try:
        g = open('{}\\backup\\diagnosis_backup.xml'.format(BASE_PATH), 'r')
    except FileNotFoundError:
        print('Fatal error!')
    else:
        f.write(g.read())
        f.close()


def get_file_path():
    path = XML_PATH
    if not os.path.exists(path):
        # possible_path = '{}\\diagnosis_backup'.format(BASE_PATH)
        # if os.path.exists(possible_path):
        #     os.rename(possible_path, path)
        # else:
        if input("Datoteka ne postoji. Želiš li ju stvoriti ovdje? (Da/Ne)").lower() == 'da':
            create_file(path)
        # return get_file_path()
    return path


def create_file(path):
    data = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<data>\n</data>'
    f = open(path, 'w')
    f.write(data)
    f.close()


def main(status=True):
    global diagnosis

    if status:
        diagnosis_name = input('\nUnesi ime dijagnoze: ')
        diagnosis_path = get_file_path()
        diagnosis = Diagnosis(diagnosis_name, diagnosis_path)
        file_backup()

    element = diagnosis.element
    # print(element)

    if element is None:
        funcs = print_menu(n=1)
    else:
        funcs = print_menu(s=1)

    while True:
        try:
            selected = int(input('Izaberi jednu od ponuđenih opcija: '))
        except ValueError:
            print("Molim unesi broj!")
        else:
            try:
                func = funcs[selected]
            except IndexError:
                print("Molim unesi broj u zadanom rasponu!")
            else:
                func()
                break

    # diagnosis.update()

    if func == on_remove_diagnosis:
        answers = print_continue_menu(s=1)
    else:
        answers = print_continue_menu()

    while True:
        ask = input("=> ").lower()
        if ask in answers:
            if ask == '':
                main(False)
                break
            elif ask == 'da':
                diagnosis.update()
                main(True)
                break
            else:
                diagnosis.update()
                return
        else:
            print("Molim unesi ispravan odgovor!")


# print(BASE_PATH)
FUNCS = [on_add_diagnosis, on_remove_diagnosis, on_diagnosis_name, on_add_symptom, on_remove_symptom, on_get_category, on_set_category,
         on_get_symptoms, on_set_name, preview, file_backup, file_fix]


print('\n{0}DIAGNOSIS  MANAGER{0}\n'.format(21 * ' '))
main()
