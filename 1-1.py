## Задание 1
'''
Пользователь вводит две переменных x и y типа int. Необходимо вывести их
* сумму
* разность x и y
* произведение
* деление x на y
* остаток от деления x на y
* x в степени y
программа должна выводить подробный вывод, реализованный при помощи f-строк.
'''

def valid_input(s):
    try:
        x, y = map(int, s.split())
        return True
    except ValueError:
        return False
        
s = input('Введите через пробел 2 целых числа:\n')
if not valid_input(s):
    print('Неверный ввод.')
    exit(1)
x, y = map(int, s.split())
print(f'x + y = {x+y}',
      f'x - y = {x-y}',
      f'x * y = {x*y}',
      f'x / y = {"n/a" if y==0 else f"{x/y:.2f}"}',
      f'x % y = {"n/a" if y==0 else x%y}',
      f'x ** y = {x**y}', sep='\n')
