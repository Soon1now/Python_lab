import re

def is_username(username):
    pattern = r'^[a-zA-Z][a-zA-Z0-9_.]{2,19}$'

    result = bool(re.fullmatch(pattern, username))
    if result:
        return username
    else:
        raise ValueError(f"Некорректное имя пользователя: '{username}'")

try:
    user_input = input("Введите имя пользователя: ")
    username = is_username(user_input)
    print(f"Имя пользователя: {username}")
except ValueError as e:
    print(e)
