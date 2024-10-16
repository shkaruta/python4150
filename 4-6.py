## Задание  6
'''
Напишите скрипт, который будет автоматически создавать резервные копии важных данных на вашем компьютере. Скрипт должен:
* Определить исходную директорию: Пользователь указывает путь к директории, которую необходимо резервировать.
* Определить целевую директорию: Пользователь указывает путь к директории, где будут сохраняться резервные копии.
* Создать структуру папок: Скрипт должен создавать в целевой директории папки с датой и временем создания резервной копии для организации хранения.
* Скопировать файлы и папки: Рекурсивно скопировать все файлы и поддиректории из исходной директории в новую директорию.
* сделать так, чтоб копирование отрабатывала раз в определенное время, задаваемое при начале работы.
* реализовать корректное завершение скрипта без закрытия терминала (например по написанию слова exit или по нажиманию определенных клавиш, ctrl + c)

Можно добавить дополнительный функционал при наличии времени и желания
'''


import os
import shutil
import sys
import time
from datetime import datetime

def backup(source_dir, target_dir):
    # Резервное копирование дерева файлов из source_dir в target_dir
    # Создаем папку с текущей датой и временем в имени
    backup_folder = os.path.join(target_dir, f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    print(f"Creating backup in: {backup_folder}")
    
    # Создаем директорию для резервного копирования, если она не существует
    os.makedirs(backup_folder, exist_ok=True)

    try:
        # Рекурсивно проходим по всем подкаталогам и файлам в исходном каталоге
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                # Формируем полный путь к файлу и его относительный путь
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, source_dir)
                target_file = os.path.join(backup_folder, rel_path)

                # Создаем необходимые подкаталоги в целевом каталоге
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                
                # Выводим информацию о текущем копируемом файле
                sys.stdout.write(f"\rCopying file: {file_path}")
                sys.stdout.flush()

                # Копируем файл, включая метаданные
                shutil.copy2(file_path, target_file)
        
        # Очистка строки и вывод сообщения о завершении резервного копирования
        clear_line()
        print("Backup completed successfully.")
    
    except Exception as e:
        clear_line()
        print(f"\nError during backup: {e}")
        sys.exit(1)

def clear_line():
    # Очистка строки в терминале (с запасом)
    sys.stdout.write("\r" + " " * 250 + "\r")
    sys.stdout.flush()

# Главная программа
try:
    # 1. Получение исходного каталога
    source_dir = input("Source directory to backup:\n").strip('"\'')
    if not os.path.isdir(source_dir):
        sys.exit(f"Error: Source directory '{source_dir}' does not exist.")

    # 2. Получение и проверка целевого каталога
    target_dir = input("Target directory for backups (will be created if doesn't exist):\n").strip('"\'')
    source_abs, target_abs = map(os.path.abspath, [source_dir, target_dir])

    # Проверка, находится ли целевой каталог внутри исходного
    if os.path.commonpath([source_abs]) == os.path.commonpath([source_abs, target_abs]):
        sys.exit(f"Error: Target directory '{target_dir}' cannot be inside the source directory.")

    # Создание целевого каталога, если он не существует
    os.makedirs(target_abs, exist_ok=True)

    # 3. Запрос интервала времени
    backup_interval = int(input("Time interval in seconds between backups (10-86400):\n"))
    backup_interval = min(86400, max(10, backup_interval))
    print("Press Ctrl-C to break")

    # 4. Запуск вечного цикла резервного копирования
    while True:
        backup(source_abs, target_abs)  # Запуск функции резервного копирования
        
        # Отсчет времени до следующего резервного копирования
        for remaining in range(backup_interval, 0, -1):
            clear_line()
            sys.stdout.write(f"Time until next backup: {remaining} seconds")
            sys.stdout.flush()
            time.sleep(1)
        clear_line()  # Стираем строку перед следующей итерацией

except KeyboardInterrupt:
    # Обработка прерывания пользователем
    clear_line()
    print("\nBackup process interrupted by user.")
    sys.exit(0)
except Exception as e:
    # Обработка других исключений
    clear_line()
    print(f"\nError: {e}")
    sys.exit(1)
