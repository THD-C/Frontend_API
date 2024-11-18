from fastapi import APIRouter, HTTPException
from grpc import RpcError
from pydantic import BaseModel

from src.connections import channel
from user import user_detail_pb2
from wallet import wallet_pb2, wallet_pb2_grpc


class WalletCreationData(BaseModel):
    id: str | None = None
    currency: str
    value: str | None = None
    user_id: str


class WalletUpdateData(BaseModel):
    id: str | None = None
    currency: str
    value: str
    user_id: str


class WalletsOwnerData(BaseModel):
    id: str


wallets = APIRouter()


@wallets.post("/create-wallet", responses={
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
})
def create_walllet(wallet_data: WalletCreationData):
    if wallet_data.value is None:
        wallet_data.value = "0"

    wallet_message = wallet_pb2.Wallet(**wallet_data.dict())

    try:
        stub = wallet_pb2_grpc.WalletsStub(channel)
        response: wallet_pb2.Wallet = stub.createWallet(wallet_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id is not None:
        return response

    raise HTTPException(status_code=400, detail="operation_failed")


@wallets.post("update-wallet", responses={
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
})
def update_wallet(update_wallet_data: WalletUpdateData):
    data_for_update = wallet_pb2.Wallet(**update_wallet_data.dict())

    try:
        stub = wallet_pb2_grpc.WalletsStub(channel)
        response: wallet_pb2.Wallet = stub.updateWallet(data_for_update)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id is not None:
        return {"success": True, **response}

    raise HTTPException(status_code=400, detail="operation_failed")


@wallets.get("get-wallets", responses={
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
    204: {
        "description": "User have no wallets",
        "content": {
            "application/json": {
                "example": {"detail": "no_content"}
            }
        }
    },
    200: {
        "description": "List of objects with wallets details",
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": "1",
                        "currency": "PLN",
                        "value": "250.32",
                        "user_id": "2"
                    },
                    {
                        "id":"52",
                        "currency": "USD",
                        "value":"0.52",
                        "user_id": "2"
                    }
                ]
                }
            }
        }
})
def get_wallets(user_id):
    user_data = user_detail_pb2.UserDetail(id=user_id)

    try:
        stub = wallet_pb2_grpc.WalletsStub(channel)
        response: wallet_pb2.WalletList = stub.getUsersWallets(user_data)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response is None:
        raise HTTPException(status_code=400, detail="operation_failed")
    elif response.wallets is None:
        raise HTTPException(status_code=204, detail="no_content")
    else:
        return {"wallets": response.wallets}
