import requests

# URL для GET-запроса, чтобы получить cookies и csrf_token
URL_LOGIN_PAGE = "https://scratch.mit.edu/login/"
USER_AGENT_VAL = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"


def create_session():
    """
    Создает сессию с правильным user-agent и возвращает её.
    """
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT_VAL, "Referer": URL_LOGIN_PAGE})
    return session


def get_csrf_token(session):
    """
    Получает страницу авторизации и извлекает CSRF-токен из cookies.
    """
    response_get = session.get(URL_LOGIN_PAGE)
    csrf_token = session.cookies.get("scratchcsrftoken", domain=".scratch.mit.edu")
    if csrf_token:
        print(f"Получен CSRF-токен: {csrf_token}")
    else:
        print("Не удалось получить CSRF-токен.")
    return csrf_token


def login(session, csrf_token, username, password):
    """
    Выполняет авторизацию с использованием CSRF-токена.
    """
    headers_post = {
        "User-Agent": USER_AGENT_VAL,
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/json",
        "Origin": "https://scratch.mit.edu",
        "Referer": "https://scratch.mit.edu/",
        "X-Csrftoken": csrf_token,
        "X-Requested-With": "XMLHttpRequest",
    }

    data = {"username": username, "password": password, "useMessages": True}

    response_post = session.post(URL_LOGIN_PAGE, headers=headers_post, json=data)

    return response_post


def save_response_to_file(response, filename):
    """
    Сохраняет содержимое ответа в HTML файл.
    """
    if response.status_code == 200:
        print("Вход успешно выполнен!")
        print(response.text)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
    else:
        print(f"Не удалось войти. Код статуса: {response.status_code}")
        print(response.text)


def main():
    # Создаю сессию
    session = create_session()

    # Получаю CSRF-токен
    csrf_token = get_csrf_token(session)

    # Авторизуюсь
    if csrf_token:
        response_post = login(session, csrf_token, "username", "password")

        # Сохраняю результат в файл
        save_response_to_file(response_post, "login_success_scratch.html")
    else:
        print("Произошла ошибка при получении CSRF-токена.")


if __name__ == "__main__":
    main()
