import requests

# URL для GET-запроса, чтобы получить cookies и _xsrf token
URL = "https://nn.hh.ru/account/login"
USER_AGENT_VAL = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"


def create_session():
    """
    Создает сессию с нужным user-agent и возвращает её.
    """
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT_VAL, "Referer": URL})
    return session


def get_xsrf_token(session):
    """
    Получает страницу входа и извлекает _xsrf token из cookies.
    """
    session.get(URL)
    _xsrf = session.cookies.get("_xsrf", domain=".hh.ru")
    if _xsrf:
        print(f"Получен _xsrf токен: {_xsrf}")
    else:
        print("Не удалось получить _xsrf токен.")
    return _xsrf


def login(session, _xsrf, username, password):
    """
    Выполняет авторизацию с использованием _xsrf токена.
    """
    data = {
        "backUrl": "https://nn.hh.ru/",
        "username": username,
        "password": password,
        "_xsrf": _xsrf,
        "remember": "yes",
    }

    response_post = session.post(URL, data)
    return response_post


def save_response_to_file(response, filename):
    """
    Сохраняет содержимое ответа в HTML файл.
    """
    if response.status_code == 200:
        print("Вход возможен только после прохождения 'капчи'!")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
    else:
        print(f"Не удалось войти. Код статуса: {response.status_code}")
        print(response.text)


def main():
    session = create_session()

    # Получаю _xsrf токен
    _xsrf = get_xsrf_token(session)

    # Авторизуюсь
    if _xsrf:
        response_post = login(session, _xsrf, "username", "password")

        # Сохраняем результат в файл
        save_response_to_file(response_post, "login_success_HH.html")
    else:
        print("Произошла ошибка при получении _xsrf токена.")


if __name__ == "__main__":
    main()
