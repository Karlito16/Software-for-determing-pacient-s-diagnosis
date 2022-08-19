#!/usr/bin/python3
# -*- coding: utf-8 -*-


def pretty_print(path):
    f = open(path, 'r')
    file_lines = f.readlines()

    file_string = ''
    for line in file_lines:
        file_string += line.strip()

    elem_list = file_string.split('><')

    for elem_id in range(len(elem_list)):
        elem = elem_list[elem_id]
        if not '>' in elem and '<' in elem:
            elem_list[elem_id] = elem + '>'
        elif not '<' in elem and '>' in elem:
            elem_list[elem_id] = '<' + elem
        else:
            elem_list[elem_id] = '<' + elem + '>'

    current_indent = 0
    current_root = ['']
    output = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    for elem in elem_list:  # current_root = ['root', 'element']
        elem_tag = elem.split()[0].split('>')[0].strip('<').strip('/')
        if elem_tag == current_root[-1]:
            current_indent -= 2
            current_root.pop()
            output += '{}{}\n'.format(current_indent * ' ', elem)
        elif not '/>' in elem and not '</' in elem:
            output += '{}{}\n'.format(current_indent * ' ', elem)
            current_indent += 2
            current_root.append(elem_tag)
        else:
            output += '{}{}\n'.format(current_indent * ' ', elem)

    f = open(path, 'w')
    f.write(output)
    f.close()
    # print(output)
    return output
