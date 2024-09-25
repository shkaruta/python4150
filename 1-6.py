# Задание 6 (дополнительно)
'''
пользователь вводит коэффициенты a, b и c квадратного уравнения. Напишите программу, которая выводит на экран его натуральные корни.
* рассчитываем дискриминант: D = b - 4 * a *c
*если дискриминант < 0, выводим, что корней нет
* если дискриминант равен 0, считаем один корень как b/(2a) и выводим его на экран
* если дискриминант > 0, считаем два корня как (b +/- d**0.5)/(2a) и выводим корни на экран
* найдите библиотечный метод, способный решать данную задачу
'''

def valid_input(s):
    # возвращает True, если введена валидная строка с тремя коэффициентами
    try:
        a, b, c = map(float, s.split())
        return True if a!=0 else False
    except ValueError:
        return False

s = input('Введите через пробел коэффициенты квадратного уравнения a, b и c:\n')
if not valid_input(s):
    print('Неверный ввод.')
    exit(1)
a, b, c = map(float, s.split())
d = b**2 - 4*a*c
if d < 0:
    print('Нет корней')
elif d == 0:
    print('x =', -b/(2*a))
elif d > 0:
    print('x1 =', (-b-d**0.5)/(2*a), '\nx2 =', (-b+d**0.5)/(2*a))
print('Корни полинома можно получить с помощью функции roots из модуля numpy.\n'
      'Функция принимает массив коэффициентов и возвращает массив корней.')
