import json

from fastapi import APIRouter, HTTPException
from grpc import RpcError
from pydantic import BaseModel
import bcrypt

from google.oauth2 import id_token
from google.auth.transport import requests

from src.connections import channel
from src.utils import GOOGLE_CLIENT_ID
from src.utils.auth import create_jwt_token
from user import user_pb2, user_pb2_grpc


class Credentials(BaseModel):
    email: str
    password: str


class RegisterData(BaseModel):
    username: str
    password: str
    email: str
    name: str | None = None
    surname: str | None = None
    street: str | None = None
    building: str | None = None
    city: str | None = None
    postal_code: str | None = None
    country: str | None = None


router = APIRouter()


class TokenRequest(BaseModel):
    OAuth_token: str


@router.post("/login", responses={500: {"description": "gRPC Error"}})
def login(credentials: Credentials):
    credentials = user_pb2.AuthUser(**credentials.dict())

    try:
        stub = user_pb2_grpc.UserStub(channel)
        response: user_pb2.AuthResponse = stub.Authenticate(credentials)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.success:
        jwt_data = {"id": response.id, "email": response.email, "login": response.username}
        jwt_token = create_jwt_token(jwt_data)

        endpoint_response = {"accessToken": jwt_token,
                             "authScheme": 'Bearer',
                             "email": response.email,
                             "username": response.username,
                             "id": response.id}

        return endpoint_response

    raise HTTPException(status_code=400, detail="invalid_credentials")


@router.post("/register")
def register_user(registerData: RegisterData):
    data_for_grpc = user_pb2.RegUser(**registerData.dict())

    try:
        stub = user_pb2_grpc.UserStub(channel)
        response: user_pb2.RegResponse = stub.Register(data_for_grpc)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.success is False:
        raise HTTPException(status_code=400, detail="email_or_username_occupied" )


    login_data = Credentials(email = registerData.email, password = registerData.password)
    login_response = login(login_data)
    return login_response


@router.post("/auth-google")
async def auth_google(token: TokenRequest):
    GOOGLE_ID = GOOGLE_CLIENT_ID

    try:
        token_id_info = id_token.verify_token(token.OAuth_token, requests.Request(), GOOGLE_ID)
        user_id = token_id_info.get("sub")
        email = token_id_info.get("email")
        hashed_password = bcrypt.hashpw(token_id_info.encode("uft-8"), bcrypt.gensalt()).decode('utf-8')


        register_data = RegisterData(username = user_id, email = email, password = hashed_password)

        await register_user(register_data)

        login_data = Credentials(email=email, password=hashed_password)
        login_response = login(login_data)

        return login_response

    except ValueError:
        raise HTTPException(status_code=400, detail="invalid_token")
