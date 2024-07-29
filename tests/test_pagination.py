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
    assert response.json()["pages"] == int((page * size) / size)
    assert len(response.json()) == 5


def test_users_pagination_page(app_url, users):
    size = 1
    response = requests.get(f"{app_url}/api/users/?size={size}&page={len(users["items"])}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["total"] == len(users["items"])
    assert response.json()["page"] == len(users["items"])
    assert response.json()["size"] == size
    assert response.json()["pages"] == len(users["items"])
    assert len(response.json()) == 5


def test_users_pagination_size(app_url, users):
    page = 1
    size = 100
    response = requests.get(f"{app_url}/api/users/?size={size}&page={page}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["total"] == len(users["items"])
    assert response.json()["page"] == 1 if int(len(users["items"]) // size) == 0 else int(len(users["items"]) // size)
    assert response.json()["size"] == size
    assert response.json()["pages"] == 1 if int(len(users["items"]) // size) == 0 else int(len(users["items"]) // size)
    assert len(response.json()) == 5


@pytest.mark.parametrize("page", [-1, 0, "fafaf"])
def test_invalid_page(app_url, page):
    size = 1
    response = requests.get(f"{app_url}/api/users/?size={size}&page={page}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("size", [-1, 0, "fafaf"])
def test_invalid_size(app_url, size):
    page = 1
    response = requests.get(f"{app_url}/api/users/?size={size}&page={page}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_nonexistent_page(app_url, users):
    size = 1
    response = requests.get(f"{app_url}/api/users/?size={size}&page={len(users["items"]) + 1}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["page"] == len(users["items"]) + 1
    assert response.json()["size"] == size
    assert response.json()["pages"] == response.json()["total"]
    assert response.json()["items"] == []
    assert len(response.json()) == 5


def test_nonexistent_size(app_url):
    page = 1
    size = 999
    response = requests.get(f"{app_url}/api/users/?size={size}&page={page}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_different_results_on_different_pages(app_url, users):
    size = 1
    page = 1
    first_page_response = requests.get(f"{app_url}/api/users/?size={size}&page={page}")
    second_page_response = requests.get(f"{app_url}/api/users/?size={size}&page={page + 1}")
    assert first_page_response != second_page_response
