# Хеш-таблица с двойным хешированием для разрешения коллизий
# класс HashTable с функцией изменения размера resize
# Вставка осуществляется с использованием двух хеш-функций: первая вычисляет основной индекс, а вторая добавляет смещение при возникновении коллизий
# Код для проверки таблицы позволяет пользователю добавлять или удалять значения и видеть текущую таблицу после каждого действия
# Ключи и значения в виде строк

class HashTable:
    def __init__(self, initial_size=8):
        self.size = initial_size  # Начальный размер таблицы
        self.count = 0  # Счетчик элементов в таблице
        self.table = [None] * self.size  # Таблица инициализируется пустыми значениями

    def hash1(self, key):
        # Первая хеш-функция, возвращающая индекс в пределах 256
        return hash(key) % 256

    def hash2(self, key):
        # Вторая хеш-функция для определения шага при коллизиях
        return 1 + (hash(key) % 128)

    def insert(self, key, value):
        # Добавление нового элемента в таблицу
        if self.count / self.size > 0.7:  # Если таблица заполнена более чем на 70%, расширяем её
            self.resize(self.size * 2)

        idx = self.hash1(key) % self.size  # Основной индекс по первой хеш-функции
        step = self.hash2(key)  # Шаг при коллизиях по второй хеш-функции

        # Вставка с использованием двойного хеширования при возникновении коллизий
        while self.table[idx] is not None:
            if self.table[idx][0] == key:
                self.table[idx] = (key, value)  # Обновляем значение, если ключ уже существует
                return
            idx = (idx + step) % self.size  # Переходим к новому индексу

        # Вставляем новую пару ключ-значение
        self.table[idx] = (key, value)
        self.count += 1

    def get(self, key):
        # Получение значения по ключу
        idx = self.hash1(key) % self.size
        step = self.hash2(key)

        # Поиск элемента по ключу
        while self.table[idx] is not None:
            if self.table[idx][0] == key:
                return self.table[idx][1]
            idx = (idx + step) % self.size
        return None

    def remove(self, key):
        # Удаление элемента по ключу
        idx = self.hash1(key) % self.size
        step = self.hash2(key)

        # Поиск и удаление элемента
        while self.table[idx] is not None:
            if self.table[idx][0] == key:
                self.table[idx] = None  # Удаление элемента
                self.count -= 1
                if self.count / self.size < 0.3 and self.size > 8:
                    self.resize(self.size // 2)  # Уменьшаем таблицу, если заполненность менее 30%
                return
            idx = (idx + step) % self.size

    def resize(self, new_size):
        # Изменение размера таблицы и перехеширование всех элементов
        old_table = self.table
        self.size = new_size
        self.count = 0
        self.table = [None] * self.size

        for item in old_table:
            if item is not None:
                self.insert(*item)  # Повторная вставка всех элементов

    def __str__(self):
        # Компактный вывод заполненных ячеек таблицы
        return {idx: item for idx, item in enumerate(self.table) if item is not None}.__str__()


# Код для проверки работы хеш-таблицы
hash_table = HashTable()

while True:
    action = input("Введите 'a' для добавления, 'r' для удаления или 's' для выхода: ").strip().lower()
    
    if action == "a":
        key = input("Введите ключ: ")
        value = input("Введите значение: ")
        hash_table.insert(key, value)
        print("Текущая таблица:", hash_table)

    elif action == "r":
        key = input("Введите ключ для удаления: ")
        hash_table.remove(key)
        print("Текущая таблица:", hash_table)

    elif action == "s":
        print("Завершение работы.")
        break

    else:
        print("Неверная команда. Введите 'a', 'r' или 's'.")
