## Задание 2
'''
Напишите функцию `is_prime(n)`, которая принимает число `n` и возвращает `True`, если число простое, и `False` в противном случае.
'''

def is_prime(x):
    return not any(x%i==0 for i in range(2, int(x**0.5)+1)) and x>1
numbers = list(map(int, input('Введите несколько натуральных через пробел: ').split()))
[print(n,'простое' if is_prime(n) else 'не простое') for n in numbers]
      