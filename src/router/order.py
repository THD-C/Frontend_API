from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter, HTTPException, Request
from grpc import RpcError
from pydantic import BaseModel

from src.connections import order_stub
from order import order_pb2, order_type_pb2, order_status_pb2, order_side_pb2
from src.router.wallets import create_wallet, WalletCreationData
from src.utils.auth import verify_user


class OrderDetails(BaseModel):
    currency_used_wallet_id: str  # Which currency is used i.e. BUY sth with USD, SELL BTC
    currency_target: str  # Which currency is the goal i.e. buy BTC, get USD from selling BTC
    nominal: str  # Number of units which are going to be used of currency_used_wallet_id
    cash_quantity: str | None = ""
    price: str  # Price on which user wants to perform an order
    type: str
    side: str


transaction_types_mapper = {
    "ORDER_TYPE_STOP_LOSS": order_type_pb2.OrderType.ORDER_TYPE_STOP_LOSS,
    "ORDER_TYPE_TAKE_PROFIT": order_type_pb2.OrderType.ORDER_TYPE_TAKE_PROFIT,
    "ORDER_TYPE_INSTANT": order_type_pb2.OrderType.ORDER_TYPE_INSTANT
}

transaction_side_mapper = {
    "ORDER_SIDE_BUY": order_side_pb2.ORDER_SIDE_BUY,
    "ORDER_SIDE_SELL": order_side_pb2.ORDER_SIDE_SELL
}

order = APIRouter(tags=["Order"])


@order.post("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Creation of order failed",
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
        "description": "Details of created order",
        "content": {
            "application/json": {
                "example": {
                    "id": "4",
                    "userId": "1",
                    "dateCreated": "2024-12-04T14:26:53.030635Z",
                    "dateExecuted": "1970-01-01T00:00:00Z",
                    "status": "ORDER_STATUS_PENDING",
                    "nominal": "10.0",
                    "price": "50.0",
                    "type": "ORDER_TYPE_INSTANT",
                    "side": "ORDER_SIDE_BUY",
                    "cryptoWalletId": "3",
                    "fiatWalletId": "2"
                }
            }
        }
    }
}, description='Creates an order')
def create_order(orderDetails: OrderDetails, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    order_type_order_details = transaction_types_mapper.get(orderDetails.type)
    order_side_order_details = transaction_side_mapper.get(orderDetails.side)

    if order_type_order_details is None or order_side_order_details is None:
        raise HTTPException(status_code=400, detail="operation_failed")

    crypto_wallet_request_data = WalletCreationData(currency=orderDetails.currency_target)
    try:
        wallet_creation_response = create_wallet(wallet_data=crypto_wallet_request_data,
                                                 request=request)
    except HTTPException as e:
        raise e

    orderRequest = order_pb2.OrderDetails(user_id=jwt_payload.get("id"),
                                          status=order_status_pb2.ORDER_STATUS_PENDING,
                                          fiat_wallet_id=orderDetails.currency_used_wallet_id,
                                          crypto_wallet_id=wallet_creation_response.get("id"),
                                          nominal=orderDetails.nominal,
                                          cash_quantity=orderDetails.cash_quantity,
                                          price=orderDetails.price,
                                          type=order_type_order_details,
                                          side=order_side_order_details
                                          )

    try:
        response: order_pb2.OrderDetails = order_stub.CreateOrder(orderRequest)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id != "":
        return MessageToDict(response)

    raise HTTPException(status_code=400, detail="operation_failed")


@order.get("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Getting order failed",
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
        "description": "Details of requested order",
        "content": {
            "application/json": {
                "example": {
                    "id": "4",
                    "userId": "1",
                    "dateCreated": "2024-12-04T14:26:53.030635Z",
                    "dateExecuted": "1970-01-01T00:00:00Z",
                    "status": "ORDER_STATUS_PENDING",
                    "nominal": "10.0",
                    "price": "50.0",
                    "type": "ORDER_TYPE_INSTANT",
                    "side": "ORDER_SIDE_BUY",
                    "cryptoWalletId": "3",
                    "fiatWalletId": "2"
                }
            }
        }
    }
}, description='Returns an order for specified order_id')
def get_order(order_id, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    order_message = order_pb2.OrderID(id=order_id)

    try:
        response: order_pb2.OrderDetails = order_stub.GetOrder(order_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id == "":
        raise HTTPException(status_code=204)
    else:
        if str(jwt_payload.get("id")) != response.user_id:
            raise HTTPException(status_code=401, detail="unauthorized_user_for_method")
        return MessageToDict(response)


@order.delete("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Deletion of order failed",
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
        "description": "Details of deleted order",
        "content": {
            "application/json": {
                "example": {
                    "id": "4",
                    "userId": "1",
                    "dateCreated": "2024-12-04T14:26:53.030635Z",
                    "dateExecuted": "1970-01-01T00:00:00Z",
                    "status": "ORDER_STATUS_PENDING",
                    "nominal": "10.0",
                    "price": "50.0",
                    "type": "ORDER_TYPE_INSTANT",
                    "side": "ORDER_SIDE_BUY",
                    "cryptoWalletId": "3",
                    "fiatWalletId": "2"
                }
            }
        }
    }
}, description='Creates an order for specifiec currency')
def delete_order(order_id, request: Request):
    get_order(order_id, request=request)

    delete_order_message = order_pb2.OrderID(id=order_id)

    try:
        response: order_pb2.OrderDetails = order_stub.DeleteOrder(delete_order_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id == "":
        raise HTTPException(status_code=400, detail="operation_failed")
    else:
        return MessageToDict(response)


@order.get("/orders", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Creation of order failed",
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
        "description": "List of objects with wallets details",
        "content": {
            "application/json": {
                "example": {
                    "orders": [
                        {
                            "id": "4",
                            "userId": "1",
                            "dateCreated": "2024-12-04T14:26:53.030635Z",
                            "dateExecuted": "1970-01-01T00:00:00Z",
                            "status": "ORDER_STATUS_PENDING",
                            "nominal": "10.0",
                            "price": "50.0",
                            "type": "ORDER_TYPE_INSTANT",
                            "side": "ORDER_SIDE_BUY",
                            "cryptoWalletId": "3",
                            "fiatWalletId": "2"
                        }, {
                            "id": "4",
                            "userId": "1",
                            "dateCreated": "2024-12-04T14:26:53.030635Z",
                            "dateExecuted": "1970-01-01T00:00:00Z",
                            "status": "ORDER_STATUS_PENDING",
                            "nominal": "10.0",
                            "price": "50.0",
                            "type": "ORDER_TYPE_INSTANT",
                            "side": "ORDER_SIDE_BUY",
                            "cryptoWalletId": "3",
                            "fiatWalletId": "5"
                        }
                    ]}

            }
        }
    }
}, description='Returns all orders bonded with user')
def get_orders(request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    user_message = order_pb2.UserID(id=jwt_payload.get("id"))

    try:
        response: order_pb2.OrderList = order_stub.GetOrderList(user_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if len(response.orders) == 0:
        raise HTTPException(status_code=204)
    else:
        return MessageToDict(response)