import random  

def generate_random_word_list():
    # Функция для генерации списка случайных слов.
    random_words = [
        "tree", "mountain", "river", "cloud", "book", 
        "chair", "light", "window", "phone", "mirror", 
        "sky", "dream", "road", "smile", "shadow"
    ]
    return random_words  

def calculate_word_weight(word):
    # Функция для вычисления веса слова.
    # Вес слова определяется как сумма значений Unicode всех его символов.
    return sum(ord(char) for char in word)  

def create_weighted_word_list(word_list):
    # Функция для создания списка словарей с весами слов и их сортировки.
    weighted_list = [{calculate_word_weight(word): word} for word in word_list]
    # Сортируем список по весам (ключам словарей)
    return sorted(weighted_list, key=lambda x: list(x.keys())[0])

def binary_search_by_weight(weighted_list, target_weight):
    # Функция для бинарного поиска по весу.
    left, right = 0, len(weighted_list) - 1  # Устанавливаем границы поиска

    while left <= right:  # Пока границы не пересекутся
        mid = (left + right) // 2  # Находим середину
        mid_weight = list(weighted_list[mid].keys())[0]
        
        # Проверяем, совпадает ли вес
        if mid_weight == target_weight:
            return mid  # Возвращаем индекс, если вес совпадает
        elif mid_weight < target_weight:
            left = mid + 1  # Сужаем поиск в правую половину
        else:
            right = mid - 1  # Сужаем поиск в левую половину

    return None  # Если не найдено, возвращаем None

def binary_search_word(weighted_list, target_word):
    # Функция для бинарного поиска слова в списке с учетом веса.
    # Сначала вычисляем вес искомого слова.
    target_weight = calculate_word_weight(target_word)
    # бинарный поиск значения target_weight
    index = binary_search_by_weight(weighted_list, target_weight)  

    if index is not None:  # индекс найден
        mid_word = weighted_list[index][target_weight]
        if mid_word == target_word:
            return index, target_weight, mid_word  # Слово найдено
    return None, target_weight, target_word  # Если слово не найдено

# Основная программа
word_list = generate_random_word_list()  # Генерируем список слов
weighted_word_list = create_weighted_word_list(word_list)  # Создаем и сортируем список весов

print("Для завершения введите 0")  # Уведомление для пользователя
# Запрашиваем слово для поиска у пользователя
while (search_word := input("Введите слово для поиска: ").strip().lower()) != '0':
    # ищем слово
    index, weight, found_word = binary_search_word(weighted_word_list, search_word)
    # Выводим результат
    if index is not None:
        print(f"Слово '{found_word}' найдено на индексе {index} с весом {weight}.")
    else:
        print(f"Слово '{search_word}' не найдено.")  
