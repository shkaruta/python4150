## Задание 5
'''
Дан список множеств. Необходимо вернуть их пересечение. 
Например, при входном списке [{1, 2, 3}, {2, 3, 4}, {3, 4, 5}], результатом должно быть {3}.
'''
lst = [{1, 2, 3}, {2, 3, 4}, {3, 4, 5}]
print('List of sets:', lst, '\nIntersection:', set.intersection(*lst))