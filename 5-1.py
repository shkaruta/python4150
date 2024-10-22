# Бронирование номеров разного класса в отеле для одного или нескольких человек (с тестированием)
from enum import Enum

# Перечисление для типов номеров
class RoomType(Enum):
    STANDARD = "Standard"
    BUDGET = "Budget"
    DELUXE = "De luxe"

# Базовый класс Номер
class Room:
    def __init__(self, room_id: int, room_type: RoomType, max_guests: int, price_per_day: float):
        self._room_id = room_id  # идентификатор номера
        self._room_type = room_type  # тип номера (перечисление)
        self._max_guests = max_guests  # максимальное количество гостей
        self._price_per_day = price_per_day  # стоимость за сутки
        self._is_available = True  # доступность номера
        self._current_guests = {}  # словарь гостей

    # Свойства только для чтения
    @property
    def room_id(self):
        return self._room_id

    @property
    def is_available(self):
        return self._is_available

    @property
    def current_guests(self):
        return self._current_guests

    def book(self, guest_id: int, num_guests: int):
        """ Бронирование номера для гостя """
        if not self._is_available:
            return False
        if num_guests > self._max_guests:
            return False

        # Успешное бронирование
        self._is_available = False
        self._current_guests[guest_id] = num_guests
        return True

    def release(self, guest_id: int):
        """ Освобождение номера гостем """
        if guest_id not in self._current_guests:
            return False

        del self._current_guests[guest_id]
        if not self._current_guests:
            self._is_available = True
        return True

# Класс Стандарт
class StandardRoom(Room):
    def __init__(self, room_id: int, num_beds: int, price_per_day: float):
        super().__init__(room_id, RoomType.STANDARD, num_beds, price_per_day)
        self._num_beds = num_beds

# Класс Эконом
class BudgetRoom(StandardRoom):
    def __init__(self, room_id: int, num_beds: int, price_per_day: float):
        super().__init__(room_id, num_beds, price_per_day)
        self._room_type = RoomType.BUDGET  # Явно устанавливаем тип комнаты
        self._available_beds = num_beds

    def book(self, guest_id: int, num_guests: int):
        """ Бронирование эконом-номера с учетом доступных кроватей """
        if num_guests > self._available_beds:
            return False

        self._available_beds -= num_guests
        self._current_guests[guest_id] = num_guests
        if self._available_beds == 0:
            self._is_available = False
        return True

    def release(self, guest_id: int):
        """ Освобождение эконом-номера """
        if guest_id not in self._current_guests:
            return False

        num_guests = self._current_guests.pop(guest_id)
        self._available_beds += num_guests
        if self._available_beds > 0:
            self._is_available = True
        return True

# Класс Люкс
class DeluxeRoom(Room):
    def __init__(self, room_id: int, num_rooms: int, has_balcony: bool, price_per_day: float):
        super().__init__(room_id, RoomType.DELUXE, num_rooms, price_per_day)
        self._num_rooms = num_rooms
        self._has_balcony = has_balcony

# Класс Отель
class Hotel:
    def __init__(self):
        self.rooms = {}  # словарь номеров, ключ - id номера

    def add_room(self, room: Room):
        self.rooms[room.room_id] = room
        print(f"Room {room.room_id} added to hotel. Type {room._room_type.value}, max guests {room._max_guests}, price {room._price_per_day}.")

    def remove_room(self, room_id: int):
        if room_id in self.rooms:
            del self.rooms[room_id]
            print(f"Room {room_id} removed from hotel.")

    # Метод для поиска доступных номеров
    def find_available_rooms(self, num_people: int = 1, room_type: RoomType = None, price_range: tuple = None):
        available_rooms = []
        for room in self.rooms.values():
            # Проверяем, доступен ли номер
            if not room.is_available:
                continue
            # Фильтруем по типу номера, если задан
            if room_type and room._room_type != room_type:
                continue
            # Фильтруем по цене, если указан диапазон
            if price_range and not (price_range[0] <= room._price_per_day <= price_range[1]):
                continue
            # Проверяем вместимость
            if num_people > room._max_guests:
                continue
            available_rooms.append(room)
        return available_rooms

    def find_occupied_rooms(self):
        """ Возвращает список занятых номеров """
        return [room for room in self.rooms.values() if not room.is_available]

# Класс Гость
class Guest:
    _guest_counter = 1  # защищенный счетчик ID гостей

    def __init__(self, full_name: str, phone_number: str, num_people: int):
        self._guest_id = Guest._guest_counter
        Guest._guest_counter += 1
        self._full_name = full_name
        self._phone_number = phone_number
        self._num_people = num_people
        self._booked_room = None

    # Свойства только для чтения
    @property
    def guest_id(self):
        return self._guest_id

    def book(self, hotel: Hotel, room_type: RoomType = None, price_range: tuple = None):
        """ Бронирование комнаты для гостя """
        rooms_found = hotel.find_available_rooms(self._num_people, room_type, price_range)
        if rooms_found:
            room = rooms_found[0]  # будем бронировать первый из подходящих
            if room.book(self._guest_id, self._num_people):
                self._booked_room = room
                print(f"Guest {self._full_name} booked room #{room.room_id}, {room._room_type.value} for {self._num_people} people for ${room._price_per_day} per day")
                return True
            else:
                print(f"Guest {self._full_name} could not book room {room.room_id}.")
                return False
        else:
            print(f"No rooms requested for guest {self._full_name}.")
            return False

        """ Освобождение забронированной комнаты """
    def release(self):
        if self._booked_room:
            self._booked_room.release(self._guest_id)
            print(f"Guest {self._full_name} released room {self._booked_room.room_id}.")
            self._booked_room = None
        else:
            print(f"Guest {self._full_name} has no room to release.")

# Тестирование

print("\nСоздание отеля")
hotel = Hotel()

print("Добавление номеров")
rooms = [
StandardRoom(1, 2, 100),
StandardRoom(2, 3, 120),
BudgetRoom(3, 4, 40),
BudgetRoom(4, 6, 30),
DeluxeRoom(5, 2, True, 400)
]
for room in rooms:
    hotel.add_room(room)

print("\nСоздание гостей")
guest1 = Guest("Иванов", "+7 123 456 7890", 1)
guest2 = Guest("Петров", "+7 098 765 4321", 3)
guest3 = Guest("Сидоров", "+7 111 111 1111", 5)
guest4 = Guest("Смирнов", "+7 222 222 2222", 2)
guest5 = Guest("Грум-Гржимайло", "+7 555 555 5555", 2)
for i, guest in enumerate([guest1, guest2, guest3, guest4, guest5]):
    print(f"Guest{i+1}: {guest._full_name}, {guest._phone_number}, {guest._num_people} people")
print("\nТесты поиска и бронирования номеров")
# Для бронирования используется метод guest.book(hotel, room_type, price_range)
# Для демонстрации того, какие номера были найдены для бронирования, вызывается функция hotel.find_available_rooms
print("Тест 1: гость 1 бронирует стандартный номер с ценой до 150")
print("Ожидаем найти room1 и room2, бронируем room1")
available_rooms = hotel.find_available_rooms(num_people=2, room_type=RoomType.STANDARD, price_range=(0, 150))
for room in available_rooms:
    print(f"Найден номер {room.room_id}, цена: {room._price_per_day}")
guest1.book(hotel, room_type=RoomType.STANDARD, price_range=(0, 150))

print("\nТест 2: гость 2 бронирует номер с ценой до 50")
print("Ожидаем найти эконом room3 и room4, бронируем 3")
available_rooms = hotel.find_available_rooms(num_people=3, price_range=(0, 50))
for room in available_rooms:
    print(f"Найден номер {room.room_id}, цена: {room._price_per_day}")
guest2.book(hotel, price_range=(0, 50))

print("\nТест 3: гость 4 бронирует стандартный номер с ценой до 100 (нет подходящих номеров)")
guest4.book(hotel, room_type=RoomType.STANDARD, price_range=(0, 100))

print("\nТест 4: Гость 2 освобождает номер")
guest2.release()

print("\nТест 5: Гость 2 освобождает незабронированный номер. Должны получить ошибку.")
guest2.release()

print("\nТест 6: Гость 4 бронирует эконом номер для 2 человек по цене до 50")
print("Ожидаем найти room3 и room4, бронируем room3")
available_rooms = hotel.find_available_rooms(num_people=2, room_type=RoomType.BUDGET, price_range=(0, 50))
for room in available_rooms:
    print(f"Найден номер {room.room_id}, цена: {room._price_per_day}")
guest4.book(hotel, room_type=RoomType.BUDGET, price_range=(0, 50))

print("\nТест 7: гость 3 бронирует номер на 5 человек класса эконом")
print("Ожидаем найти room4 и бронируем его")
available_rooms = hotel.find_available_rooms(num_people=5, room_type=RoomType.BUDGET)
for room in available_rooms:
    print(f"Найден номер {room.room_id}, цена: {room._price_per_day}")
guest3.book(hotel, room_type=RoomType.BUDGET)

print("\nТест 8: гость 5 бронирует номер класса люкс с ценой до 500")
print("Ожидаем найти room5 и бронируем его")
available_rooms = hotel.find_available_rooms(num_people=1, room_type=RoomType.DELUXE, price_range=(0, 500))
for room in available_rooms:
    print(f"Найден номер {room.room_id}, цена: {room._price_per_day}")
guest5.book(hotel, room_type=RoomType.DELUXE, price_range=(0, 500))

print("\nТест 9: ищем все доступные номера")
print("Ожидаем найти 2 (standard), 3 (budget), 4 (budget), последние два свободны частично")
available_rooms = hotel.find_available_rooms()
for room in available_rooms:
    print(f"{room._room_type.value} #{room.room_id}, for {room._max_guests} guests, available for {room._max_guests - sum(room.current_guests.values())}, price ${room._price_per_day} per day")
