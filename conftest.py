import time
import pytest
import requests
from selenium import webdriver
from home_page import HomePage
from login_page import LoginPage


@pytest.fixture(scope="class")
def init_driver(request):
    # Инициализация драйвера

    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    request.cls.driver = driver

    # Инициализация страницы
    login_page = LoginPage(driver)
    home_page = HomePage(driver)

    # Открытие страницы
    login_page.open_login_page()

    # Логинимся
    login_page.login_user()
    time.sleep(10)

    # Заходим на сервер диплом
    home_page.clic_to_server_diplow()
    time.sleep(5)
    # Переходим в канал "6"
    home_page.clic_to_channel()
    time.sleep(5)
    yield driver
    driver.quit()


@pytest.fixture(scope="class")
def base_url():
    return 'https://discord.com/login'


@pytest.fixture(scope="class")
def base_url():
    return 'https://discord.com/login'


@pytest.fixture(scope="class")
def base_url():
    return 'https://discord.com/login'


@pytest.fixture(scope="module")
def base_url():
    return "https://discord.com/api/v10"


@pytest.fixture(scope="module")
def channel_id():
    return 1286673475565518878


@pytest.fixture(scope="module")
def headers():
    token = "MTI4NjYwOTgxOTEzNzk5ODg4Mw.G0Fflc.xDvykECWDsrG8htMuEj9KYG0lUdx_XweIdzOsE"
    return {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }


@pytest.fixture
def message_id(base_url, channel_id, headers):
    # Создание сообщения перед каждым тестом
    url = f"{base_url}/channels/{channel_id}/messages"
    data = {
        "content": "Калды Балды."
    }
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 200, f"Failed to create message: {response.text}"
    message_id = response.json().get('id')
    yield message_id  # Возвращаем message_id для использования в тестах

    # Удаление сообщения после теста
    delete_url = f"{base_url}/channels/{channel_id}/messages/{message_id}"
    response = requests.delete(delete_url, headers=headers)
    assert response.status_code == 204, f"Failed to delete message: {response.text}"
