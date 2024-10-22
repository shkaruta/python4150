import random

class Node:
    def __init__(self, value, parent=None):
        self.value = value  # Значение узла
        self.left = None  # Ссылка на левого потомка
        self.right = None  # Ссылка на правого потомка
        self.parent = parent  # Ссылка на родительский узел

class BinarySearchTree:
    def __init__(self):
        self.root = None  # Корневой узел

    def _create_node(self, value, parent=None):
        # Создает и возвращает новый узел
        return Node(value, parent)
    def _merge_subtrees(self, node):
        # удаляет узел node и склеивает оставшиеся ветки дерева
        if node.left is None and node.right is None:  # Если у узла нет потомков
            if node.parent:  # Если узел не корень
                if node == node.parent.left:
                    node.parent.left = None  # Удаляем связь с левым потомком
                else:
                    node.parent.right = None  # Удаляем связь с правым потомком
            else:
                self.root = None  # Если узел корень, делаем дерево пустым

        elif node.left is None:  # Если есть только правый потомок
            if node.parent:  # Если узел не корень
                if node == node.parent.left:
                    node.parent.left = node.right  # Присваиваем правого потомка
                else:
                    node.parent.right = node.right
            else:  # Если узел является корнем
                self.root = node.right  # Правый потомок становится новым корнем
            node.right.parent = node.parent  # Устанавливаем ссылку на родителя у потомка

        elif node.right is None:  # Если есть только левый потомок
            if node.parent:  # Если узел не корень
                if node == node.parent.left:
                    node.parent.left = node.left  # Присваиваем левого потомка
                else:
                    node.parent.right = node.left
            else:  # Если узел является корнем
                self.root = node.left  # Левый потомок становится новым корнем
            node.left.parent = node.parent  # Устанавливаем ссылку на родителя у потомка

        else:  # Если у узла два потомка
            successor = self._find_min(node.right)  # Ищем минимальный элемент в правом поддереве
            node.value = successor.value  # Замещаем удаляемый узел минимальным
            self._merge_subtrees(successor)  # Удаляем преемника

    def _find_min(self, node):
        # Возвращает узел с минимальным значением в дереве, считая от узла node
        current = node
        while current.left:  # Идем по левым потомкам
            current = current.left
        return current

    def _find_max(self, node):
        # Возвращает узел с максимальным значением в дереве, считая от узла node
        current = node
        while current.right:  # Идем по правым потомкам
            current = current.right
        return current

    def insert(self, value):
        # добавляет элемент в дерево
        if self.root is None:
            self.root = self._create_node(value)  # Если дерево пустое, создаем корень
        else:
            current = self.root
            parent = None
            while current:  # Ищем место для вставки нового элемента
                parent = current
                if value < current.value:
                    current = current.left  # Идем влево
                else:
                    current = current.right  # Идем вправо
            if value < parent.value:
                parent.left = self._create_node(value, parent)  # Создаем левого потомка
            else:
                parent.right = self._create_node(value, parent)  # Создаем правого потомка

    def delete(self, value):
        # удаляет элемент, вызывая функцию _merge_subtrees 
        node = self.search(value)
        if node:
            self._merge_subtrees(node)  # Удаляем найденный элемент
            print(f"Элемент {value} удален.")  
        else:
            print(f"Значение {value} не найдено в дереве.")  

    def search(self, value):
        # Поиск элемента в дереве
        current = self.root
        while current:
            if value == current.value:
                return current  # Возвращаем узел, если нашли значение
            elif value < current.value:
                current = current.left  # Идем влево
            else:
                current = current.right  # Идем вправо
        return None  # Возвращаем None, если элемент не найден

    def _inorder_traversal(self, node, result):
        # Симметричный обход дерева
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.value)
            self._inorder_traversal(node.right, result)

    def print_tree(self):
        # Печать дерева в виде отсортированного списка
        result = []
        self._inorder_traversal(self.root, result)
        print("Tree:", result)  # Вывод отсортированного дерева
        print(f"Root: {self.root.value}" if self.root else "root = None")


class CLI:
    def __init__(self):
        self.bst = BinarySearchTree()  # Создаем бинарное дерево

    def run(self):
        # Основной цикл для работы через CLI
        while True:
            command = input("Введите команду (a - add, d - delete, s - search, p - print, t - test, e - exit): ").lower()

            if command in  ["add", "a"]:
                self.handle_insert()
            elif command in ["delete", "d"]:
                self.handle_delete()
            elif command in ["search", "s"]:
                self.handle_search()
            elif command in ["print", "p"]:
                self.handle_print()
            elif command in ["test", "t"]:
                self.handle_test()
            elif command in ["exit", "e"]:
                print("Завершение работы.")
                break
            else:
                print("Неизвестная команда.")  

    def handle_insert(self):
        try:
            value = int(input("Введите значение для добавления: "))
            self.bst.insert(value)
            print(f"Элемент {value} добавлен.")
        except ValueError:
            print("Некорректный ввод.")  # Сообщение об ошибке, если введено не число

    def handle_delete(self):
        try:
            value = int(input("Введите значение для удаления: "))
            self.bst.delete(value)
        except ValueError:
            print("Некорректный ввод.")  # Сообщение об ошибке, если введено не число

    def handle_search(self):
        try:
            value = int(input("Введите значение для поиска: "))
            node = self.bst.search(value)
            if node:
                print(f"Элемент {value} найден.")
            else:
                print(f"Элемент {value} не найден.")
        except ValueError:
            print("Некорректный ввод.")  # Сообщение об ошибке, если введено не число

    def handle_print(self):
        # Печать дерева
        self.bst.print_tree()

    def handle_test(self):
        # Тестирование
        print("Тестирование бинарного дерева на подготовленном наборе данных")
        # 1. Генерация списка случайных целых чисел от 0 до 100 длиной 20
        n=10
        min_n=0
        max_n=100
        numbers = random.sample(range(min_n, max_n+1), n)
        # 2. Вывод списка на экран
        print(f"Случайные числа от {min_n} до {max_n}:\n{numbers}")
        print("Будем добавлять их по одному в дерево")
        # 3. Создание дерева и печать пустого дерева
        bst = BinarySearchTree()
        bst.print_tree()

        # 4. Добавление чисел в дерево по одному и печать дерева после каждого добавления
        for num in numbers:
            print(f"Добавляем {num}")
            bst.insert(num)
            bst.print_tree()

        # 5. Поиск элемента (найдём случайный элемент списка)
        num = numbers[random.randint(0,len(numbers)-1)]
        print(f"Найдем случайный существующий элемент {num}")
        search_value = num
        found_node = bst.search(search_value)
        if found_node:
            print(f"Элемент {search_value} найден.")
        else:
            print(f"Элемент {search_value} не найден.")

        # 6. Поиск несуществующего элемента (например, 200)
        print("Ищем несуществующий элемент 200")
        search_value = 200
        found_node = bst.search(search_value)
        if found_node:
            print(f"Элемент {search_value} найден.")
        else:
            print(f"Элемент {search_value} не найден.")

        # 7. Удаление случайного существующего элемента
        print(f"Удаляем существующий элемент {num}")
        delete_value = num
        bst.delete(delete_value)
        bst.print_tree()

        # 8. Попытка удаления несуществующего элемента (например, 200)
        print("Удаляем несуществующий элемент 200")
        delete_value = 200
        bst.delete(delete_value)

        # 9 Удаление корня
        print(f"Удаление коренного элемента {bst.root.value}")
        delete_value = bst.root.value
        bst.delete(delete_value)
        bst.print_tree()

        # 10 Удаление минимального элемента
        print(f"Удаление минимального элемента {bst._find_min(bst.root).value}")
        delete_value = bst._find_min(bst.root).value
        bst.delete(delete_value)
        bst.print_tree()

        # 11 Удаление максимального элемента
        print(f"Удаление максимального элемента {bst._find_max(bst.root).value}")
        delete_value = bst._find_max(bst.root).value
        bst.delete(delete_value)
        bst.print_tree()

cli = CLI()
cli.run()
