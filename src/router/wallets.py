from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter, HTTPException, Request, Query
from grpc import RpcError
from pydantic import BaseModel

from src.connections import wallet_stub
from src.router.currency import get_currency_type
from user import user_type_pb2
from wallet import wallet_pb2
from src.utils.auth import verify_user

from src.utils.logger import logger


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


def is_crypto_func(currency_type):
    if currency_type == "NOT_SUPPORTED":
        return None
    elif currency_type == "FIAT":
        return False
    else:
        return True


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
                "example": [{"detail": "operation_failed"},
                            {"detail": "negative_value"},
                            {"detail": "currency_type_not_supported"}
                            ]
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
                    "user_id": "2",
                    "is_crypto": False
                }
            }
        }
    }
}, description='Returns details about created or existing wallet')
def create_wallet(wallet_data: WalletCreationData, request: Request):
    wallet_value = float(wallet_data.value)
    if wallet_value < 0:
        raise HTTPException(400, detail="negative_value")

    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    currency_type_info = get_currency_type(wallet_data.currency)
    is_crypto = is_crypto_func(currency_type_info["currency_type"])

    if (is_crypto and wallet_value > 0) and jwt_payload["user_type"] < user_type_pb2.USER_TYPE_SUPER_ADMIN_USER:
        logger.warning("User tried to create crypto wallet with value > 0")
        raise HTTPException(400, detail = "operation_failed")

    if is_crypto is None:
        raise HTTPException(400, detail="currency_type_not_supported")

    wallet_message = wallet_pb2.Wallet(**wallet_data.model_dump(), user_id=jwt_payload.get("id"), is_crypto=is_crypto)

    try:
        response = wallet_stub.CreateWallet(wallet_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id != "":
        logger.info("Creating wallet successfully performed")
        return MessageToDict(response, preserving_proto_field_name=True, always_print_fields_with_no_presence=True)
    logger.warning("Wallet creation failed")
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
                "example": [{"detail": "operation_failed"},
                            {"detail": "negative_value"}]
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
                    "user_id": "2",
                    "is_crypto": False
                }
            }
        }
    }
}, description="Update of wallet. Fields id and value are obligatory.")
def update_wallet(update_wallet_data: WalletUpdateData, request: Request):
    get_wallet_by_id(update_wallet_data.id, request)
    wallet_value = float(update_wallet_data.value)

    if wallet_value < 0:
        raise HTTPException(400, detail="negative_value")

    update_wallet_data.value = str(float(wallet_value) + float(update_wallet_data.value))

    data_for_update = wallet_pb2.Wallet(**update_wallet_data.model_dump())

    try:
        response: wallet_pb2.Wallet = wallet_stub.UpdateWallet(data_for_update)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id != "":
        logger.info("Updated wallet")
        return MessageToDict(response, preserving_proto_field_name=True, always_print_fields_with_no_presence=True)
    logger.info("Failed to update wallet")
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
                            {"detail": "unauthorized_user_for_method"}
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
                            "user_id": "2",
                            "is_crypto": False
                        },
                        {
                            "id": "52",
                            "currency": "USD",
                            "value": "0.52",
                            "user_id": "2",
                            "is_crypto": False
                        }
                    ]
                }
            }
        }
    }
}, description="Returns a list of all wallets which belong to user")
def get_wallets(request: Request,
                user_id: str = Query(None, description="ID of the user")):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    if user_id is None or jwt_payload.get("id") == user_id:
        user_data = wallet_pb2.UserID(id=jwt_payload.get("id"))
    elif jwt_payload.get("user_type") >= user_type_pb2.USER_TYPE_SUPER_ADMIN_USER:
        user_data = wallet_pb2.UserID(id=user_id)
    else:
        logger.warning("Unauthorized user tried to fetch list of wallets")
        raise HTTPException(401, detail="unauthorized_user_for_method")

    try:
        response: wallet_pb2.WalletList = wallet_stub.GetUsersWallets(user_data)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if len(response.wallets) == 0:
        logger.info("No wallets found")
        raise HTTPException(status_code=204)
    else:
        logger.info("Found wallets")
        return MessageToDict(response, preserving_proto_field_name=True, always_print_fields_with_no_presence=True)


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
            "application/json": [
                {"detail": "operation_failed"},
                {"detail": "wallet_id_incorrect_value"}
            ]
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
                    "user_id": "2",
                    "is_crypto": False
                }
            }
        }
    }
}, description="Returns wallet details of specified id")
def get_wallet_by_id(wallet_id, request: Request):
    if wallet_id is None or int(wallet_id) <= 0:
        raise HTTPException(status_code=400, detail="wallet_id_incorrect_value")

    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    wallet_data = wallet_pb2.Wallet(id=wallet_id)

    try:
        response: wallet_pb2.Wallet = wallet_stub.GetWallet(wallet_data)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id == "":
        logger.info("No wallet with given id")
        raise HTTPException(status_code=204)

    if str(jwt_payload.get("id")) != response.user_id and jwt_payload.get(
            "user_type") < user_type_pb2.USER_TYPE_SUPER_ADMIN_USER:
        logger.warning("Unauthorized user tried to fetch wallet details")
        raise HTTPException(status_code=401, detail="unauthorized_user_for_method")
    logger.info(f"Fetched wallet with id: {wallet_id}")
    return MessageToDict(response, preserving_proto_field_name=True, always_print_fields_with_no_presence=True)


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
        "description": "Deleting wallet with given id failed",
        "content": {
            "application/json": {
                "example": [{"detail": "operation_failed"},
                            {"detail": "wallet_id_incorrect_value"}
                            ]
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
        "description": "No such wallet"
    },
    200: {
        "description": "Details of removed wallet",
        "content": {
            "application/json": {
                "example": {
                    "id": "1",
                    "currency": "PLN",
                    "value": "250.32",
                    "user_id": "2",
                    "is_crypto": False
                }
            }
        }
    }
}, description="Deletes wallet of specified id")
def delete_wallet(wallet_id, request: Request):
    if int(wallet_id) <= 0:
        raise HTTPException(status_code=400, detail="wallet_id_incorrect_value")

    try:
        wallet_data = get_wallet_by_id(wallet_id=wallet_id, request=request)
    except HTTPException as e:
        logger.warning(f"Problems with fetching wallet: {e}")
        raise e

    try:
        wallet_id_message = wallet_pb2.Wallet(id=wallet_data.get("id"))
        response: wallet_pb2.Wallet = wallet_stub.DeleteWallet(wallet_id_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id == "":
        logger.warning(f"Deleting wallet failed")
        raise HTTPException(status_code=204)
    logger.info(f"Deleted wallet: {wallet_id}")
    return MessageToDict(response, preserving_proto_field_name=True, always_print_fields_with_no_presence=True)
