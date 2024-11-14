import jwt
from datetime import datetime, timedelta, UTC

from src.utils import JWT_SECRET_KEY


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10


def create_jwt_token(data: dict):
    data['iat'] = datetime.now(UTC).isoformat()
    data['exp'] = (datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).isoformat()
    return jwt.encode(data, JWT_SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError | jwt.InvalidTokenError:
        return None

def refresh_jwt_token(token: str):
    payload = verify_jwt_token(token)
    if payload is not None:
        payload['iat'] = datetime.now(UTC)
        payload['exp'] = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return payload
    return None


