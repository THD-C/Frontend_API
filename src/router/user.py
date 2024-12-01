from fastapi import APIRouter, HTTPException, Request
from google.protobuf.json_format import MessageToDict
from grpc import RpcError
from pydantic import BaseModel

from src.connections import channel
from src.utils.auth import verify_user
from user import user_pb2, user_pb2_grpc

user = APIRouter(tags=['User'])


class UpdateUserData(BaseModel):
    email: str
    name: str
    surname: str
    street: str
    building: str
    city: str
    postal_code: str
    country: str


class DeleteUser(BaseModel):
    password: str
    mail: str | None = ""


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str


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
                    "username": "sed ullamco",
                    "email": "new@mail.com",
                    "name": "some",
                    "surname": "adipisicing in in ex",
                    "street": "dolore",
                    "building": "sit amet dolor",
                    "city": "tempor quis aliquip",
                    "postalCode": "cillum cupidatat mollit laborum",
                    "country": "non mollit irure"
                }
            }
        }
    }
}, description="Returns user details")
def get_user_details(request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    user_message = user_pb2.ReqGetUserDetails(id=jwt_payload.get("id"), )
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
        return MessageToDict(response, preserving_proto_field_name=True)


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

    user_message = user_pb2.ReqUpdateUser(**update_data.dict(), id=jwt_payload.get("id"))
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
        return MessageToDict(user_message, preserving_proto_field_name=True)


@user.put("/update-password",responses={
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
                "example": {"detail": "invalid_old_password"}
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
    200: {
        "description": "Success of operation",
        "content": {
            "application/json": {
                "example": {
                    "success": "true",
                }
            }
        }
    }
}, description="Updates password")
def update_password(updatePassword: UpdatePassword, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    password_message: user_pb2.ChangePass = user_pb2.ChangePass(**updatePassword.dict(), login=jwt_payload.get("email"))

    try:
        stub = user_pb2_grpc.UserStub(channel)
        response: user_pb2.ResultResponse = stub.ChangePassword(password_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.success is False:
        raise HTTPException(status_code=400, detail="invalid_old_password")

    return MessageToDict(response, preserving_proto_field_name=True)


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
        "description": "Details and success about the deleting user's profile",
        "content": {
            "application/json": {
                "example": {
                    "success": "bool",
                    "id": "str"
                }
            }
        }
    }
}, description="Deletes user")
def delete_user(userDelete: DeleteUser, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    if userDelete.mail == "":
        userDelete.mail = jwt_payload.get("email")

    user_message = user_pb2.ReqDeleteUser(**userDelete.dict(), id=jwt_payload.get("id"))
    try:
        stub = user_pb2_grpc.UserStub(channel)
        response: user_pb2.ResultResponse = stub.Delete(user_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.success is False:
        raise HTTPException(status_code=400, detail="operation_failed")
    else:
        return MessageToDict(response, preserving_proto_field_name=True)
