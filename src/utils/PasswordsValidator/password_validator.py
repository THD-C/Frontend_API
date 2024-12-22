from fastapi import HTTPException
from argon2 import PasswordHasher
from grpc import RpcError
from src.utils.logger import logger
from src.connections import password_stub
from password import password_pb2
from src.utils.auth import JWT_SECRET_KEY


def hash_password(password):
    ph = PasswordHasher()
    return ph.hash(password, salt=bytes(JWT_SECRET_KEY, 'utf-8'))

def validate_password(password: str) -> bool:
    if len(password) < 12:
        raise ValueError("password_length_too_short")

    common_password_message: password_pb2.PasswordMessage = password_pb2.PasswordMessage(password=password)
    try:
        isCommonPassword: password_pb2.CheckResponse = password_stub.CheckPassword(common_password_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if isCommonPassword.isCommon:
        raise ValueError("common_password")

    return isCommonPassword.isCommon
