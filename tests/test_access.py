from fastapi.testclient import TestClient

from main import app

import tests.helpers.auth_helper as auth_helper
from src.router.access import Credentials, RegisterData
from src.utils.auth import verify_jwt_token
from user.user_pb2 import ReqDeleteUser

client = TestClient(app)


def test_register_new_user():
    response = client.post(url="/api/auth/register", json=auth_helper.register_user_1.model_dump())
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["email"] == auth_helper.register_user_1.email
    assert json_response["username"] == auth_helper.register_user_1.username
    assert json_response["authScheme"] == "Bearer"


def test_register_existing_user():
    response = client.post(url="/api/auth/register", json=auth_helper.register_user_1.model_dump())
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["detail"] == "email_or_username_occupied"


def test_login_user_username():
    response = client.post(url="/api/auth/login", json=auth_helper.login_user_1.model_dump())
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["email"] == auth_helper.register_user_1.email
    assert json_response["username"] == auth_helper.register_user_1.username
    assert json_response["authScheme"] == "Bearer"


def test_login_invalid_login():
    response = client.post(url="/api/auth/login", json=auth_helper.login_invalid_login_1.model_dump())
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["detail"] == "invalid_credentials"


def test_login_invalid_email():
    response = client.post(url="/api/auth/login", json=auth_helper.login_invalid_email_login_1.model_dump())
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["detail"] == "invalid_credentials"


def test_login_invalid_password():
    response = client.post(url="/api/auth/login", json=auth_helper.login_invalid_password_1.model_dump())
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["detail"] == "invalid_credentials"


def test_login_user_email():
    response = client.post(url="/api/auth/login", json=auth_helper.email_login_user_1.model_dump())
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["email"] == auth_helper.register_user_1.email
    assert json_response["username"] == auth_helper.register_user_1.username
    assert json_response["authScheme"] == "Bearer"
 