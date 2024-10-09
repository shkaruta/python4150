## Задание 4
'''
Напишите функцию, которая читает текстовый файл и подсчитывает количество строк, слов и символов в файле. 
Программа должна также вернуть самое длинное слово в файле и его длину. 
На вход функции можно подавать название файла (будем считать что он находится в той же директории, что и скрипт), 
выход можно оформить словарем с соответствующими ключами.
'''

from string import punctuation
def read_file(file_name):
    line_count = word_count = char_count = 0
    longest_word = ''
    with open(file_name, encoding='utf-8') as file:
        for line in file:
            line_count += 1
            word_count += len(line.split())  # считаем словом любую последовательность символов, разделенных пробелами
            char_count += len(line)  # cr считаем, lf не считаем
            cleaned_line = ''.join(c for c in line if c not in punctuation.replace('-',''))  # дефис - не пунктуация
            longest_word = max(cleaned_line.split() + [longest_word], key=len)
    return line_count, word_count, char_count, longest_word, len(longest_word)

file_name = input('Введите имя файла: ')
strings = ('Lines:', 'Words:', 'Chars:', 'Longest word:', 'Longest len:')
[print(s, v) for s,v in zip(strings, read_file(file_name))]
