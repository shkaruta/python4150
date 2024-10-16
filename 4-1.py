## Задание 1
'''
Напишите программу, которая считывает текстовый файл, 
находит все электронные почты и номера телефонов с помощью регулярных выражений, 
а затем сохраняет найденные данные в новый файл.
'''

import re

# мейлы и телефоны захватываются, если они отграничены как слова (\b)
# практически все требования rfc для мейлов, tld  на существование не проверяются 
email_pattern = r"\b[a-zA-Z0-9#\$%&'*+/=?^_`{|}~]+(?:\.[a-zA-Z0-9#\$%&'*+/=?^_`{|}~]+)*@(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,}\b"
# для рф, 7, 8 или ничего, возможен лидирующий плюс, возможны дефисы, один или два пробела между группами, скобки вокруг первой группы, или вообще без разделяющих знаков
phone_pattern = r"\b(?:\+7|8)?\s*(?:\(\d{3}\)|\d{3})[\s\-]{0,2}\d{3}[\s\-]{0,2}\d{2}[\s\-]{0,2}\d{2}|\b\d{3}[\s\-]{0,2}\d{3}[\s\-]{0,2}\d{4}\b"
output_filename = 'output.txt'

def find_contacts(input_filename, output_filename, email_pattern, phone_pattern):
    # Принимает имена входного и выходного файла, строки regexp для мейла и телефона
    # Читает вход по строкам, записывает найденные мейлы и телефоны в выход
    # Компилируем регулярки в regex objects
    email_regex = re.compile(email_pattern)
    phone_regex = re.compile(phone_pattern)
    with open(output_filename, 'wt', encoding='utf-8') as output_file, \
        open(input_filename, encoding='utf-8') as input_file:
        for line in input_file:
            emails = email_regex.findall(line)
            phones = phone_regex.findall(line)
            if emails or phones:
                for email in emails:
                    output_file.write(f"{email}\n")
                for phone in phones:
                    output_file.write(f"{phone}\n")

input_filename = input('Введите имя входного файла: ')
find_contacts(input_filename, output_filename, email_pattern, phone_pattern)
