## Задание 5
'''
Напишите программу, которая генерирует случайные пароли заданной длины, включающие 
буквы верхнего и нижнего регистра, 
цифры и 
специальные символы.
'''

import random as r
import string as s
# строка, из которой будем выбирать символы для пароля 
charset = s.ascii_letters + s.digits + s.punctuation

def gen_pass(length):
    # возвращает случайную строку длиной length, выбирая по крайней мере по одному lowercase, uppercase, digit, punctuation
    # сначала по одному из каждой группы, потом добираем остальное
    pwd = [r.choice(c) for c in (s.ascii_lowercase, s.ascii_uppercase, s.digits, s.punctuation)] + \
    [r.choice(charset) for _ in range(4, length)]
    r.shuffle(pwd)
    return ''.join(pwd)

def gen_passwords(length, count):
    # возвращает множество count уникальных паролей длиной length при помощи функции gen_pass
    passwords = set()
    while len(passwords) < count:
        passwords.add(gen_pass(length))
    return passwords

length = int(input('Введите длину пароля (6-20): '))
length = min(20, max(6, length))
count = int(input('Введите число паролей (1-10): '))
count= min(10, max(1, count))
print(*gen_passwords(length, count), sep='\n')
