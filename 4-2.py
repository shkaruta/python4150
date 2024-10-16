## Задание 2
'''
Напишите скрипт, который отправляет GET-запрос к API https://api.github.com/users/{username} 
(где `{username}` — имя пользователя на GitHub), 
получает JSON-ответ и 
выводит на экран имя пользователя, его логин и количество репозиториев
'''

import requests

def get_github_user_info(username):
    # URL for the GitHub API
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the JSON response
        user_data = response.json()
        name = user_data.get('name', 'Name not available')
        login = user_data.get('login', 'Username not available')
        public_repos = user_data.get('public_repos', 'No repo information')
        print(f"Name: {name}")
        print(f"Username: {login}")
        print(f"Number of public repositories: {public_repos}")
    else:
        print(f"Failed to fetch information for user {username}. Status code: {response.status_code}")

username = input('Имя пользователя на github: ')
get_github_user_info(username)
