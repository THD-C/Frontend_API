from fastapi import APIRouter, HTTPException
from src.connections import channel
from src.utils.auth import create_jwt_token
from user import user_pb2, user_pb2_grpc

router = APIRouter()

@router.post("/login/")
def login(email: str, password: str):
    if email is None or password is None:
         raise HTTPException(status_code=400, detail="Invalid credentials")

    credentials = user_pb2.AuthUser(email=email, password=password)
    stub = user_pb2_grpc.UserStub(channel)
    response:user_pb2.AuthResponse = stub.Authenticate(credentials)
    if response and response.success:
        jwt_data = {"id": response.id, "email": response.email, "login": response.username}
        jwt_token = 'Bearer ' + create_jwt_token(jwt_data)



