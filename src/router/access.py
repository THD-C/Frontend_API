from fastapi import APIRouter, HTTPException
from Frontend_API.src.connections import channel
from Frontend_API.src.grpc_generated.user import user_pb2, user_pb2_grpc

router = APIRouter()

@router.post("/login")
async def login(username: str, password: str):
    if username is None or password is None:
         raise HTTPException(status_code=400, detail="Invalid credentials")

    credentials = user_pb2.Us
