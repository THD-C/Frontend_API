from fastapi import APIRouter, HTTPException, Request
from google.protobuf.json_format import MessageToDict
from grpc import RpcError
from pydantic import BaseModel

from src.connections import channel
from src.utils.auth import verify_user
from user import user_pb2, user_pb2_grpc

user = APIRouter(tags=['User'])


class UpdateUserData(BaseModel):
    id: str
    email: str
    password: str
    name: str
    surname: str
    street: str
    building: str
    city: str
    postal_code: str
    country: str


@user.get("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    401: {
        "description": "Authorization failure",
        "content": {
            "application/json": {
                "example": [{"detail": "no_authorization_header"},
                            {"detail": "invalid_auth_scheme"},
                            {"detail": "invalid_token"},
                            {"detail": "expired_token"},
                            {"detail": "unauthorized_user_for_method"}
                            ]

            }
        }
    },
    204: {
        "description": "No user with given id"
    },
    200: {
        "description": "Details of specified user",
        "content": {
            "application/json": {
                "example": {
                    "id": "1",
                    "currency": "PLN",
                    "value": "250.32",
                    "user_id": "2"
                }
            }
        }
    }
}, description="Returns user details of specified id")
def get_user_details(user_id, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)
    if str(jwt_payload.get("id")) != user_id:
        raise HTTPException(status_code=401, detail="unauthorized_user_for_method")

    user_message = user_pb2.ReqGetUserDetails(id=user_id)
    try:
        stub = user_pb2_grpc.UserStub(channel)
        response: user_pb2.UserDetails = stub.GetUserDetails(user_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.username == "":
        raise HTTPException(status_code=204)
    else:
        return MessageToDict(response)


@user.put("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Update of details failed",
        "content": {
            "application/json": {
                "example": {"detail": "operation_failed"}
            }
        }
    },
    401: {
        "description": "Authorization failure",
        "content": {
            "application/json": {
                "example": [{"detail": "no_authorization_header"},
                            {"detail": "invalid_auth_scheme"},
                            {"detail": "invalid_token"},
                            {"detail": "expired_token"},
                            {"detail": "unauthorized_user_for_method"}
                            ]

            }
        }
    },
    204: {
        "description": "No user with given id"
    },
    200: {
        "description": "Details of specified user after update",
        "content": {
            "application/json": {
                "example": {
                    "id": "string",
                    "password": "string",
                    "name": "string",
                    "surname": "string",
                    "street": "string",
                    "building": "string",
                    "city": "string",
                    "postal_code": "string",
                    "country": "string"
                }
            }
        }
    }
}, description="Updates user details of specified id")
def update_user_details(update_data: UpdateUserData, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)
    if str(jwt_payload.get("id")) != update_data.id:
        raise HTTPException(status_code=401, detail="unauthorized_user_for_method")

    user_message = user_pb2.ReqUpdateUser(**update_data.dict())
    try:
        stub = user_pb2_grpc.UserStub(channel)
        response: user_pb2.ResultResponse = stub.Update(user_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.success is False:
        raise HTTPException(status_code=400, detail="operation_failed")
    else:
        after_update_data =  MessageToDict(user_message)
        after_update_data.pop("password")
        return after_update_data



@user.delete("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    401: {
        "description": "Authorization failure",
        "content": {
            "application/json": {
                "example": [{"detail": "no_authorization_header"},
                            {"detail": "invalid_auth_scheme"},
                            {"detail": "invalid_token"},
                            {"detail": "expired_token"},
                            {"detail": "unauthorized_user_for_method"}
                            ]

            }
        }
    },
    204: {
        "description": "No user with given id"
    },
    200: {
        "description": "Details of specified user after update",
        "content": {
            "application/json": {
                "example": {
                    "success": "bool",
                    "id": "str"
                }
            }
        }
    }
}, description="Deletes user with specified id")
def delete_user(user_id, request:Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)
    if str(jwt_payload.get("id")) != user_id:
        raise HTTPException(status_code=401, detail="unauthorized_user_for_method")

    user_message = user_pb2.ReqDeleteUser(id=user_id)
    try:
        stub = user_pb2_grpc.UserStub(channel)
        response: user_pb2.ResultResponse = stub.Update(user_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.success is False:
        raise HTTPException(status_code=400, detail="operation_failed")
    else:
        return MessageToDict(response)