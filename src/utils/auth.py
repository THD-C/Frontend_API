import jwt
from datetime import datetime, timedelta, UTC
from grpc import RpcError
from fastapi import HTTPException

from src.connections import secret_stub
from secret import secret_pb2

from src.utils.logger import logger

try:
    message = secret_pb2.SecretName(name = "JWT_SECRET_KEY")
    response_secret: secret_pb2.SecretValue = secret_stub.GetSecret(message)
    JWT_SECRET_KEY = response_secret.value
except RpcError as err:
    logger.error(f"Error retrieving secret: {err}")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_jwt_token(data: dict):
    data['iat'] = datetime.now(UTC)
    data['exp'] = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(data, JWT_SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        logger.error(f"Problems with token: {e}")
        raise e

def refresh_jwt_token(token: str):
    payload = verify_jwt_token(token)
    if payload is not None:
        payload['iat'] = datetime.now(UTC)
        payload['exp'] = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return payload
    return None

def verify_user(authorization_header: str):
    if authorization_header is None:
        logger.warning("No authorization header provided")
        raise HTTPException(status_code=401, detail="no_authorization_header")
    try:
        if authorization_header.startswith("Bearer "):
            token = authorization_header.split(" ")[1]
            payload = verify_jwt_token(token)
        else:
            logger.warning("Invalid authorization scheme")
            raise HTTPException(status_code=401, detail = "invalid_auth_scheme")
    except jwt.ExpiredSignatureError:
        logger.warning("Expired token")
        raise HTTPException(
            status_code=401,
            detail="expired_token"
        )
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
        raise HTTPException(
            status_code=401,
            detail="invalid_token"
        )
    return payload

