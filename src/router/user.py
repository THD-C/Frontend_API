from enum import Enum

from fastapi import APIRouter, HTTPException, Request, Query
from google.protobuf.json_format import MessageToDict
from grpc import RpcError
from pydantic import BaseModel

from src.connections import user_stub
from src.utils.auth import verify_user
from user import user_pb2, user_type_pb2

from src.utils.logger import logger
from src.utils.PasswordsValidator.password_validator import hash_password

user = APIRouter(tags=["User"])


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


class UserType(str, Enum):
    STANDARD_USER = "STANDARD_USER"
    BLOGGER_USER = "BLOGGER_USER"
    ADMIN_USER = "ADMIN_USER"

    def to_grpc(self):
        mapping = {
            self.STANDARD_USER: user_type_pb2.USER_TYPE_STANDARD_USER,
            self.BLOGGER_USER: user_type_pb2.USER_TYPE_BLOGGER_USER,
            self.ADMIN_USER: user_type_pb2.USER_TYPE_SUPER_ADMIN_USER,
        }
        return mapping[self]


@user.get(
    "/",
    responses={
        500: {
            "description": "Problems occurred inside the server",
            "content": {
                "application/json": {"example": {"detail": "internal_server_error"}}
            },
        },
        401: {
            "description": "Authorization failure",
            "content": {
                "application/json": {
                    "example": [
                        {"detail": "no_authorization_header"},
                        {"detail": "invalid_auth_scheme"},
                        {"detail": "invalid_token"},
                        {"detail": "expired_token"},
                        {"detail": "unauthorized_user_for_method"},
                    ]
                }
            },
        },
        204: {"description": "No user with given id"},
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
                        "country": "non mollit irure",
                    }
                }
            },
        },
    },
    description="Returns user details",
)
def get_user_details(request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    user_message = user_pb2.ReqGetUserDetails(id=jwt_payload.get("id"))
    try:
        response: user_pb2.UserDetails = user_stub.GetUserDetails(user_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.username == "":
        logger.warning("No user found")
        raise HTTPException(status_code=204)
    else:
        logger.info("User's details found")
        return MessageToDict(
            response,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True,
        )


@user.put(
    "/",
    responses={
        500: {
            "description": "Problems occurred inside the server",
            "content": {
                "application/json": {"example": {"detail": "internal_server_error"}}
            },
        },
        400: {
            "description": "Update of details failed",
            "content": {
                "application/json": {"example": {"detail": "operation_failed"}}
            },
        },
        401: {
            "description": "Authorization failure",
            "content": {
                "application/json": {
                    "example": [
                        {"detail": "no_authorization_header"},
                        {"detail": "invalid_auth_scheme"},
                        {"detail": "invalid_token"},
                        {"detail": "expired_token"},
                        {"detail": "unauthorized_user_for_method"},
                    ]
                }
            },
        },
        204: {"description": "No user with given id"},
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
                        "country": "string",
                    }
                }
            },
        },
    },
    description="Updates user details of specified id",
)
def update_user_details(update_data: UpdateUserData, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    user_message = user_pb2.ReqUpdateUser(
        **update_data.model_dump(), id=jwt_payload.get("id")
    )
    try:
        response: user_pb2.ResultResponse = user_stub.Update(user_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.success is False:
        logger.warning("Updating user details failed")
        raise HTTPException(status_code=400, detail="operation_failed")
    else:
        logger.info("Updating user details completed")
        return MessageToDict(
            user_message,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True,
        )


@user.put(
    "/update-password",
    responses={
        500: {
            "description": "Problems occurred inside the server",
            "content": {
                "application/json": {"example": {"detail": "internal_server_error"}}
            },
        },
        400: {
            "description": "Update of details failed",
            "content": {
                "application/json": {"example": {"detail": "invalid_old_password"}}
            },
        },
        401: {
            "description": "Authorization failure",
            "content": {
                "application/json": {
                    "example": [
                        {"detail": "no_authorization_header"},
                        {"detail": "invalid_auth_scheme"},
                        {"detail": "invalid_token"},
                        {"detail": "expired_token"},
                        {"detail": "unauthorized_user_for_method"},
                    ]
                }
            },
        },
        200: {
            "description": "Success of operation",
            "content": {
                "application/json": {
                    "example": {
                        "success": "true",
                    }
                }
            },
        },
    },
    description="Updates password",
)
def update_password(updatePassword: UpdatePassword, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    password_message: user_pb2.ChangePass = user_pb2.ChangePass(
        login=jwt_payload.get("email"),
        old_password=hash_password(updatePassword.old_password),
        new_password=hash_password(updatePassword.new_password),
    )

    try:
        response: user_pb2.ResultResponse = user_stub.ChangePassword(password_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.success is False:
        logger.info("User passed wrong old password")
        raise HTTPException(status_code=400, detail="invalid_old_password")

    logger.info("Changing password completed")
    return MessageToDict(
        response,
        preserving_proto_field_name=True,
        always_print_fields_with_no_presence=True,
    )


@user.delete(
    "/",
    responses={
        500: {
            "description": "Problems occurred inside the server",
            "content": {
                "application/json": {"example": {"detail": "internal_server_error"}}
            },
        },
        401: {
            "description": "Authorization failure",
            "content": {
                "application/json": {
                    "example": [
                        {"detail": "no_authorization_header"},
                        {"detail": "invalid_auth_scheme"},
                        {"detail": "invalid_token"},
                        {"detail": "expired_token"},
                        {"detail": "unauthorized_user_for_method"},
                    ]
                }
            },
        },
        204: {"description": "No user with given id"},
        200: {
            "description": "Details and success about the deleting user's profile",
            "content": {
                "application/json": {"example": {"success": "bool", "id": "str"}}
            },
        },
    },
    description="Deletes user",
)
def delete_user(request: Request,
        user_id: int = Query(..., description="ID of the user to delete"),):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)
    
    '''
        Write validation if user who request to delete user is super admin
    '''

    user_message = user_pb2.ReqDeleteUser(
        id=user_id
    )
    try:
        response: user_pb2.ResultResponse = user_stub.Delete(user_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.success is False:
        logger.warning("Deleting user failed")
        raise HTTPException(status_code=400, detail="operation_failed")
    else:
        logger.info("User deleted")
        return MessageToDict(response, preserving_proto_field_name=True)


@user.get(
    "/list-users",
    responses={
        500: {
            "description": "Problems occurred inside the server",
            "content": {
                "application/json": {"example": {"detail": "internal_server_error"}}
            },
        },
        401: {
            "description": "Authorization failure",
            "content": {
                "application/json": {
                    "example": [
                        {"detail": "no_authorization_header"},
                        {"detail": "invalid_auth_scheme"},
                        {"detail": "invalid_token"},
                        {"detail": "expired_token"},
                        {"detail": "unauthorized_user_for_method"},
                    ]
                }
            },
        },
        204: {"description": "No users found"},
        200: {
            "description": "List of all users",
            "content": {
                "application/json": {
                    "example": {
                        "user_data": [
                            {
                                "ID": "1",
                                "email": "admin@thdc.pl",
                                "username": "admin",
                                "user_type": "USER_TYPE_SUPER_ADMIN_USER",
                            }
                        ]
                    }
                }
            },
        },
    },
    description="Lists users for administrative purposes",
)
def list_users(request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    if jwt_payload["user_type"] < user_type_pb2.USER_TYPE_SUPER_ADMIN_USER:
        logger.warning("Unauthorized user tried to fetch list of wallets")
        raise HTTPException(401, detail="unauthorized_user_for_method")

    try:
        response: user_pb2.UsersList = user_stub.GetAllUsers(user_pb2.AllUsersRequest())
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if len(response.user_data) == 0:
        logger.info("No users found")
        raise HTTPException(status_code=204)
    else:
        return MessageToDict(
            response,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True,
        )


@user.put(
    "/change-user-type",
    responses={
        500: {
            "description": "Problems occurred inside the server",
            "content": {
                "application/json": {"example": {"detail": "internal_server_error"}}
            },
        },
        401: {
            "description": "Authorization failure",
            "content": {
                "application/json": {
                    "example": [
                        {"detail": "no_authorization_header"},
                        {"detail": "invalid_auth_scheme"},
                        {"detail": "invalid_token"},
                        {"detail": "expired_token"},
                        {"detail": "unauthorized_user_for_method"},
                    ]
                }
            },
        },
        204: {"description": "No user with given id"},
        200: {
            "description": "Details and success about update operation",
            "content": {
                "application/json": {"example": {"success": "bool", "id": "str"}}
            },
        },
    },
    description="Provides managing users' types for administrative purposes. User type can be change only by administrator user.",
)
def change_user_type(
    request: Request,
    new_user_type: UserType,
    user_id: str = Query(description="User ID whose type will be changed."),
):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    if jwt_payload["user_type"] < user_type_pb2.USER_TYPE_SUPER_ADMIN_USER:
        logger.warning("Unauthorized user tried to change user type")
        raise HTTPException(status_code=401, detail="unauthorized_user_for_method")

    issued_user_details_message: user_pb2.ReqGetUserDetails = (
        user_pb2.ReqGetUserDetails(id=user_id)
    )
    try:
        issued_user_details: user_pb2.UserDetails = user_stub.GetUserDetails(
            issued_user_details_message
        )
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if issued_user_details.username == "":
        raise HTTPException(status_code=204)

    if issued_user_details.username == jwt_payload["login"]:
        logger.warning("User tried to take user type from his own")
        raise HTTPException(status_code=401, detail="unauthorized_user_for_method")
    else:
        update_message: user_pb2.ReqUpdateUser = user_pb2.ReqUpdateUser(
            id=user_id, user_type=new_user_type.to_grpc()
        )
        try:
            update_response: user_pb2.UserDetails = user_stub.Update(update_message)
        except RpcError as e:
            logger.error("gRPC error details:", e)
            raise HTTPException(status_code=500, detail="internal_server_error")

        return MessageToDict(
            update_response,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True,
        )
