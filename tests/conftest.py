import os
from http import HTTPStatus

import requests
import dotenv
import pytest


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture
def app_url():
    return f"http://{os.getenv("APP_URL")}:{os.getenv("APP_PORT")}"


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()
