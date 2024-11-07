# Базовый http-сервер
from flask import Flask, jsonify, request

# создаём приложение Flask
app = Flask(__name__)

# главная страница
@app.route('/')
def home():
    return "Hello, this is the home page!"

# маршрут для возврата JSON-ответа
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "message": "This is some data from the server",
        "status": "success"
    }
    return jsonify(data)

# маршрут для обработки POST-запроса
@app.route('/api/submit', methods=['POST'])
def submit_data():
    data = request.json  # Получаем JSON-данные из запроса
    response = {
        "received_data": data,
        "message": "Data received successfully"
    }
    return jsonify(response), 201  # Возвращаем JSON с кодом ответа 201 (Created)

# функция для вычисления факториала
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# маршрут для вычисления факториала
@app.route('/factorial', methods=['GET'])
def calculate_factorial():
    # Получаем параметр из запроса
    number_str = request.args.get('number')
    
    # Проверка: существует ли параметр и является ли он целым числом от 1 до 100
    if not number_str or not number_str.isdigit():
        return "Введите целое число от 1 до 100", 400  # Ошибка 400 — неверный запрос

    number = int(number_str)
    if number < 1 or number > 100:
        return "Введите целое число от 1 до 100", 400  # Ошибка 400 — неверный запрос

    # Если проверка пройдена, вычисляем факториал
    fact = factorial(number)
    return f"Введено число {number}<br>{number}! = {fact}", 200

# запуск сервера
if __name__ == '__main__':
    app.run(debug=True)


# проверка запросов в powershell
'''
проверка get-запроса в powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000/api/data -Method GET
проверка вычисления факториала
Invoke-WebRequest -Uri "http://127.0.0.1:5000/factorial?number=5" -Method GET
проверка post-запроса
$headers = @{"Content-Type"="application/json"}
$body = '{"key": {"username": "john_doe", "email": "john@example.com"}}'  # JSON-данные о пользователе
Invoke-WebRequest -Uri http://127.0.0.1:5000/api/submit -Method POST -Headers $headers -Body $body
'''
