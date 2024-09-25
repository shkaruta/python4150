## Задание 3
'''
Пользователь вводит список чисел. Если пользователь набирает -1, ввод заканчивается. Необходимо
* вывести длину списка
* вывести сумму элементов в списке (решить через циклы и через метод списка)
* вывести только четные элементы списка
'''

def is_int(s):
    # Возвращает True, если строка s представляет собой  целое число
    if '.' in s:
        return False
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    # Возвращает True, если строка s представляет собой  вещественное число
    if '.' not in s:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False

lst = []
print('Введите список чисел по одному в строке.\nДля завершения введите -1.')
while (num := input().strip()) != '-1':
    if is_int(num):
        lst.append(int(num))
    elif is_float(num):
        lst.append(float(num))
total = 0
for item in lst:
    total += item
print('Длина списка:', len(lst))
print('Сумма элементов списка через цикл for:', total)
print('Сумма элементов через функцию sum:', sum(lst))
print('Четные элементы:', *[item for item in lst if type(item) is int and item%2==0])
