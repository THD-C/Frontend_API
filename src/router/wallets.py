from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter, HTTPException, Request
from grpc import RpcError
from pydantic import BaseModel

from src.connections import  wallet_stub
from user import user_detail_pb2
from wallet import wallet_pb2
from src.utils.auth import verify_user


class WalletCreationData(BaseModel):
    id: str | None = ""
    currency: str
    value: str | None = "0"


class WalletUpdateData(BaseModel):
    id: str
    currency: str | None = ""
    value: str


class WalletsOwnerData(BaseModel):
    id: str


wallets = APIRouter(tags=["Wallets"])


@wallets.post("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Creation of wallet failed",
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
    200: {
        "description": "Details of created wallet",
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
}, description='Returns details about created or existing wallet')
def create_wallet(wallet_data: WalletCreationData, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    wallet_message = wallet_pb2.Wallet(**wallet_data.dict(), user_id=jwt_payload.get("id"))

    try:
        response = wallet_stub.CreateWallet(wallet_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id != "":
        return MessageToDict(response, preserving_proto_field_name=True)

    raise HTTPException(status_code=400, detail="operation_failed")


@wallets.put("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Update of wallet failed",
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
    200: {
        "description": "Details of the wallet after update",
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
}, description="Update of wallet. Fields id and value are obligatory.")
def update_wallet(update_wallet_data: WalletUpdateData, request: Request):
    wallet_details = get_wallet_by_id(update_wallet_data.id, request)
    wallet_value = float(wallet_details["value"])

    update_wallet_data.value = str(float(wallet_value) + float(update_wallet_data.value))

    data_for_update = wallet_pb2.Wallet(**update_wallet_data.dict())

    try:
        response: wallet_pb2.Wallet = wallet_stub.UpdateWallet(data_for_update)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id != "":
        return MessageToDict(response, preserving_proto_field_name=True)

    raise HTTPException(status_code=400, detail="operation_failed")


@wallets.get("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Getting list of wallets failed",
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
                            {"detail": "unathorized_user_for_method"}
                            ]

            }
        }
    },
    204: {
        "description": "User have no wallets"
    },
    200: {
        "description": "List of objects with wallets details",
        "content": {
            "application/json": {
                "example": {
                    "wallets": [
                        {
                            "id": "1",
                            "currency": "PLN",
                            "value": "250.32",
                            "user_id": "2"
                        },
                        {
                            "id": "52",
                            "currency": "USD",
                            "value": "0.52",
                            "user_id": "2"
                        }
                    ]
                }
            }
        }
    }
}, description="Returns a list of all wallets for user")
def get_wallets(request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    user_data = user_detail_pb2.UserDetail(id=jwt_payload.get("id"))

    try:
        response: wallet_pb2.WalletList = wallet_stub.GetUsersWallets(user_data)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if len(response.wallets) == 0:
        raise HTTPException(status_code=204)
    else:
        return MessageToDict(response, preserving_proto_field_name=True)


@wallets.get("/wallet", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Getting list of wallets failed",
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
        "description": "User have no wallets"
    },
    200: {
        "description": "Details of specified wallet",
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
}, description="Returns wallet details of specified id")
def get_wallet_by_id(wallet_id, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    wallet_data = wallet_pb2.Wallet(id=wallet_id)

    try:
        response: wallet_pb2.Wallet = wallet_stub.GetWallet(wallet_data)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id == "":
        raise HTTPException(status_code=204)

    if str(jwt_payload.get("id")) != response.user_id:
        raise HTTPException(status_code=401, detail="unauthorized_user_for_method")

    return MessageToDict(response, preserving_proto_field_name=True)


@wallets.delete("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Getting list of wallets failed",
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
        "description": "User have no wallets"
    },
    200: {
        "description": "Details of removed wallet",
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
}, description="Deletes wallet of specified id")
def delete_wallet(wallet_id, request: Request):
    try:
        wallet_data = get_wallet_by_id(wallet_id=wallet_id, request=request)
    except HTTPException as e:
        raise e

    try:
        wallet_id_message = wallet_pb2.Wallet(id=wallet_data.get("id"))
        response: wallet_pb2.Wallet = wallet_stub.DeleteWallet(wallet_id_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id == "":
        raise HTTPException(status_code=204)

    return MessageToDict(response, preserving_proto_field_name=True)
