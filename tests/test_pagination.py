from http import HTTPStatus

import pytest
import requests


@pytest.mark.parametrize("page, size", [(12, 1), (1, 12), (6, 2), (2, 6)])
def test_users_pagination(app_url, page, size):
    response = requests.get(f"{app_url}/api/users/?size={size}&page={page}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["total"] == page * size
    assert response.json()["page"] == page
    assert response.json()["size"] == size
    assert response.json()["pages"] == (page * size) / size
    assert len(response.json()) == 5


@pytest.mark.parametrize("page", [-1, 0, "fafaf"])
def test_invalid_page(app_url, page):
    response = requests.get(f"{app_url}/api/users/?size=1&page={page}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("size", [-1, 0, "fafaf"])
def test_invalid_size(app_url, size):
    response = requests.get(f"{app_url}/api/users/?size={size}&page=1")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
