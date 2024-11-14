from fastapi import APIRouter, HTTPException
from grpc import RpcError
import json
from pydantic import BaseModel

from src.connections import channel
from src.utils.auth import create_jwt_token
from user import user_pb2, user_pb2_grpc

class Credentials(BaseModel):
    email:str
    password:str

class RegisterData(BaseModel):
    username:str
    password:str
    email:str
    name:str | None = None
    surname:str | None = None
    street:str | None = None
    building:str | None = None
    city:str | None = None
    postal_code:str | None = None
    country:str | None = None

router = APIRouter()

@router.post("/login")
def login(credentials:Credentials):

    credentials = user_pb2.AuthUser(**credentials.dict())

    try:
        stub = user_pb2_grpc.UserStub(channel)
        response: user_pb2.AuthResponse = stub.Authenticate(credentials)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail=f"gRPC call failed: {e.details()}")

    if response.success:
        jwt_data = {"id": response.id, "email": response.email, "login": response.username}
        jwt_token = create_jwt_token(jwt_data)

        endpoint_response = {"accessToken": jwt_token,
                             "authScheme": 'Bearer',
                             "email": response.email,
                             "username": response.username}

        return endpoint_response

    raise HTTPException(status_code=400, detail="Invalid credentials")

@router.post("/register")
def register_user(registerData:RegisterData):

    data_for_grpc = user_pb2.RegUser(**registerData.dict())

    try:
        stub = user_pb2_grpc.UserStub(channel)
        response: user_pb2.RegResponse = stub.Register(data_for_grpc)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail=f"gRPC call failed: {e.details()}")

    print(response.success)

    return {"account_created": response.success}


