## Задание 5
'''
Напишите функцию `merge_files , которая принимает список путей к текстовым файлам и возвращает одну строку, содержащую объединенное содержимое всех файлов. 
Также необходимо реализовать возможность записи в файл полученного объединения 
(сделать необходимо при помощи дополнительного входного параметра True/False, по умолчанию значение True, содержимое записывается в файл).
'''

def merge_files(file_names, write_flag=True):
    output_buffer = ''
    output_file_name = 'output.txt'
    for file_name in file_names:
        with open(file_name, encoding='utf-8') as file:
            output_buffer += file.read()
    if write_flag:
        with open(output_file_name, 'wt', encoding='utf-8') as file:
            file.write(output_buffer)
    return output_buffer

file_names = input('Введите через пробел имена файлов:\n').split()
print(merge_files(file_names))
