# Выводит фамилию, мейлы и даты из текстового файла согласно регулярным выражениям
import re

filename = 'lutz.txt'
patterns = [
    # "Лутц" во всех падежах
    r'\bлутц[а-я]*\b',                  
    # нечто, похожее на email
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',  
    # дата в формате dd.mm.yyyy с разделителями точка, дефис, слеш, корректность не проверяется
    r'\b\d{1,2}[./-]\d{1,2}[./-]\d{4}\b'  
]

with open(filename, 'r', encoding='utf-8') as file:
    text = file.read()
for i, pattern in enumerate(patterns, start=1):
    matches = re.findall(pattern, text, re.IGNORECASE)
    print(f'\nРезультаты поиска {i}-го регулярного выражения ({pattern}):')
    print('Первые 10 совпадений:', ', '.join(matches[:10]))
    print('Общее количество совпадений:', len(matches))  

'''
Вывод программы:
Результаты поиска 1-го регулярного выражения (\bлутц[а-я]*\b):
Первые 10 совпадений: Лутц, Лутц, Лутц, Лутц, Лутц, Лутц, Лутцапереведены, Лутц, Лутц, Лутц
Общее количество совпадений: 13
Результаты поиска 2-го регулярного выражения (\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b):
Первые 10 совпадений: bookquestions@oreilly.com
Общее количество совпадений: 1
Результаты поиска 3-го регулярного выражения (\b\d{1,2}[./-]\d{1,2}[./-]\d{4}\b):
Первые 10 совпадений: 22.10.2010, 5/31/1963, 5/31/1963, 5/31/1963, 5/1/1963
Общее количество совпадений: 5
'''
