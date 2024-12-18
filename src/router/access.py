import hashlib

from fastapi import APIRouter, HTTPException
from grpc import RpcError
from pydantic import BaseModel

from google.oauth2 import id_token
from google.auth.transport import requests

from secret import secret_pb2
from src.connections import secret_stub, user_stub
from src.utils.auth import create_jwt_token
from user import user_pb2

from src.utils.logger import logger
from src.utils.PasswordsValidator.password_validator import hash_password, validate_password

try:
    message = secret_pb2.SecretName(name="GOOGLE_CLIENT_ID")
    response_secret: secret_pb2.SecretValue = secret_stub.GetSecret(message)
    GOOGLE_CLIENT_ID = response_secret.value
except RpcError as err:
    logger.error(f"Error retrieving secret: {err}")


class Credentials(BaseModel):
    login: str
    password: str


class RegisterData(BaseModel):
    username: str
    password: str
    email: str
    name: str | None = ""
    surname: str | None = ""
    street: str | None = ""
    building: str | None = ""
    city: str | None = ""
    postal_code: str | None = ""
    country: str | None = ""


class TokenRequest(BaseModel):
    OAuth_token: str


access = APIRouter(tags=['Auth'])


@access.post("/login", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Invalid credentials passed",
        "content": {
            "application/json": {
                "example": {"detail": "invalid_credentials"}
            }
        }
    },
    200: {
        "description": "Details about the user who got authorized",
        "content": {
            "application/json": {
                "example": {
                    "accessToken": "str",
                    "authScheme": "str",
                    "email": "xyz@gmail.com",
                    "username": "xyz"
                }
            }
        }
    }
}, description="Authorize the user who has the account already created.")
def login(credentials: Credentials):
    credentials.password = hash_password(credentials.password)
    credentials = user_pb2.AuthUser(**credentials.dict())

    try:
        response: user_pb2.AuthResponse = user_stub.Authenticate(credentials)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.success:
        jwt_data = {"id": response.id, "email": response.email, "login": response.username}
        jwt_token = create_jwt_token(jwt_data)

        endpoint_response = {"accessToken": jwt_token,
                             "authScheme": 'Bearer',
                             "email": response.email,
                             "username": response.username}
        logger.info(f"User with username: {response.username} logged in")
        return endpoint_response
    logger.warning("User not logged in - invalid credentials")
    raise HTTPException(status_code=400, detail="invalid_credentials")


@access.post("/register", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Passed data have another user assigned to it",
        "content": {
            "application/json": {
                "example": {"detail": "email_or_username_occupied"}
            }
        }
    },
    200: {
        "description": "Details about the user whose account is registered and authorized",
        "content": {
            "application/json": {
                "example": {
                    "accessToken": "str",
                    "authScheme": "str",
                    "email": "xyz@gmail.com",
                    "username": "xyz"
                }
            }
        }
    }
}, description="Create and authorize new account.")
def register_user(registerData: RegisterData):
    try:
        validate_password(registerData.password)
        registerData.password = hash_password(registerData.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data_for_grpc = user_pb2.RegUser(**registerData.dict())

    try:
        response: user_pb2.RegResponse = user_stub.Register(data_for_grpc)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.success is False:
        logger.warning("Occupied credentials for data given")
        raise HTTPException(status_code=400, detail="email_or_username_occupied")

    login_data = Credentials(login=registerData.email, password=registerData.password)
    login_response = login(login_data)
    logger.info(f"Account created successfully. Permissions granted for user {login_response["username"]}")
    return login_response


@access.post("/auth-google", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Token for OAuth is invalid",
        "content": {
            "application/json": {
                "example": {"detail": "invalid_token"}
            }
        }
    },
    200: {
        "description": "Details about the user whose account is registered and authorized",
        "content": {
            "application/json": {
                "example": {
                    "accessToken": "str",
                    "authScheme": "str",
                    "email": "xyz@gmail.com",
                    "username": "xyz"
                }
            }
        }
    }
}, description="enables access with google account")
def auth_google(token: TokenRequest):
    try:
        token_id_info = id_token.verify_token(token.OAuth_token, requests.Request(), GOOGLE_CLIENT_ID)
        user_id = token_id_info.get("sub")
        email = token_id_info.get("email")
        pass_base = user_id + email
        hashed_password = hash_password(pass_base)

        register_data = RegisterData(username=email, email=email, password=hashed_password)
        try:
            register_response = register_user(register_data)
            logger.info("Successfully registered user with gmail")

            return register_response
        except HTTPException as e:
            if e.status_code == 400:
                login_data = Credentials(login=email, password=hashed_password)
                login_response = login(login_data)
                logger.info("User logged in using google")
                return login_response
            else:
                return e

    except ValueError as e:
        logger.error(f"Error with google authorization: {e}")
        raise HTTPException(status_code=400, detail="invalid_token")
