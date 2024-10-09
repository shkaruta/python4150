## Задание 1
'''
На вход программы подается список чисел. Используя функции map, filter и reduce необходимо:
* создать новый список, элементами которого будут числа из первого списка, возведенные в третью степень
* из получившегося списка отобрать только четные элементы
* найти произведение всех элементов получившегося в п.2 списка

'''
from functools import reduce
# считаем, что на входе корректная последовательность целых
numbers = list(map(int, input('Введите несколько целых через пробел: ').split()))
print(numbers:=list(map(lambda x: x**3, numbers)))
print(numbers:=list(filter(lambda x: x%2==0, numbers)))
print(product:=reduce(lambda a,b: a*b, numbers, 1))
