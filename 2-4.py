## Задание 4
'''
Дан словарь. Необходимо поменять его ключи и значения местами. Предполагается, что все значения уникальны и могут быть ключами в новом словаре. 
Например, при входном словаре {'a': 1, 'b': 2, 'c': 3}, результатом должен быть {1: 'a', 2: 'b', 3: 'c'}.
'''
dct = {'a': 1, 'b': 2, 'c': 3}
print('dict1:', dct, '\ndict2:', {v:k for k,v in dct.items()})
