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

# запуск сервера
if __name__ == '__main__':
    app.run(debug=True)


# проверка запросов в powershell
'''
проверка get-запроса в powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000/api/data -Method GET
проверка post-запроса
$headers = @{"Content-Type"="application/json"}
$body = '{"key": {"username": "john_doe", "email": "john@example.com"}}'  # JSON-данные о пользователе
Invoke-WebRequest -Uri http://127.0.0.1:5000/api/submit -Method POST -Headers $headers -Body $body
'''
