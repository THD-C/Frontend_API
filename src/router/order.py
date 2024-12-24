from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter, HTTPException, Request
from grpc import RpcError
from pydantic import BaseModel
from enum import Enum
from typing import Optional

from src.connections import order_stub
from order import order_pb2, order_type_pb2, order_status_pb2, order_side_pb2
from src.router.wallets import create_wallet, WalletCreationData
from src.utils.auth import verify_user

from src.utils.logger import logger


class OrderType(str, Enum):
    STOP_LOSS = "ORDER_TYPE_STOP_LOSS"
    TAKE_PROFIT = "ORDER_TYPE_TAKE_PROFIT"
    INSTANT = "ORDER_TYPE_INSTANT"
    PENDING = "ORDER_TYPE_PENDING"


class OrderSide(str, Enum):
    BUY = "ORDER_SIDE_BUY"
    SELL = "ORDER_SIDE_SELL"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    PARTIALLY_COMPLETED = "PARTIALLY_COMPLETED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    IN_PROGRESS = "IN_PROGRESS"


class OrderDetails(BaseModel):
    currency_used_wallet_id: str  # Which currency is used i.e. BUY sth with USD, SELL BTC
    currency_target: str  # Which currency is the goal i.e. buy BTC, get USD from selling BTC
    nominal: str  # Number of units which are going to be used of currency_used_wallet_id
    cash_quantity: str | None = ""
    price: str  # Price on which user wants to perform an order
    type: OrderType
    side: OrderSide


transaction_types_mapper = {
    "ORDER_TYPE_STOP_LOSS": order_type_pb2.OrderType.ORDER_TYPE_STOP_LOSS,
    "ORDER_TYPE_TAKE_PROFIT": order_type_pb2.OrderType.ORDER_TYPE_TAKE_PROFIT,
    "ORDER_TYPE_INSTANT": order_type_pb2.OrderType.ORDER_TYPE_INSTANT,
    "ORDER_TYPE_PENDING": order_type_pb2.OrderType.ORDER_TYPE_PENDING
}

transaction_side_mapper = {
    "ORDER_SIDE_BUY": order_side_pb2.ORDER_SIDE_BUY,
    "ORDER_SIDE_SELL": order_side_pb2.ORDER_SIDE_SELL
}

transaction_status_mapper = {
    "PENDING": order_status_pb2.OrderStatus.ORDER_STATUS_PENDING,
    "ACCEPTED": order_status_pb2.OrderStatus.ORDER_STATUS_ACCEPTED,
    "REJECTED": order_status_pb2.OrderStatus.ORDER_STATUS_REJECTED,
    "PARTIALLY_COMPLETED": order_status_pb2.OrderStatus.ORDER_STATUS_PARTIALLY_COMPLETED,
    "COMPLETED": order_status_pb2.OrderStatus.ORDER_STATUS_COMPLETED,
    "CANCELLED": order_status_pb2.OrderStatus.ORDER_STATUS_CANCELLED,
    "EXPIRED": order_status_pb2.OrderStatus.ORDER_STATUS_EXPIRED,
    "IN_PROGRESS": order_status_pb2.OrderStatus.ORDER_STATUS_IN_PROGRESS
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
                    "id": "1",
                    "user_id": "1",
                    "date_created": "2024-12-22T11:56:35.387707Z",
                    "date_executed": "1970-01-01T00:00:00Z",
                    "status": "ORDER_STATUS_PENDING",
                    "nominal": "50.0",
                    "price": "100000.0",
                    "type": "ORDER_TYPE_INSTANT",
                    "side": "ORDER_SIDE_BUY",
                    "crypto_wallet_id": "9",
                    "fiat_wallet_id": "1"
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

    if order_type_order_details is None or order_side_order_details is None \
            or float(orderDetails.price) <= 0 or float(orderDetails.nominal) <= 0:
        logger.warning("Incorrect types provided")
        raise HTTPException(status_code=400, detail="operation_failed")

    crypto_wallet_request_data = WalletCreationData(currency=orderDetails.currency_target)
    try:
        wallet_creation_response = create_wallet(wallet_data=crypto_wallet_request_data,
                                                 request=request)
    except HTTPException as e:
        logger.warning(f"Creation wallet error: {e}")
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
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id != "":
        logger.info(f"Order with id: {response.id} placed successfully")
        return MessageToDict(response, preserving_proto_field_name=True)
    logger.warning("Placing order failed")
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
                    "id": "1",
                    "user_id": "1",
                    "date_created": "2024-12-22T11:56:35.387707Z",
                    "date_executed": "1970-01-01T00:00:00Z",
                    "status": "ORDER_STATUS_PENDING",
                    "nominal": "50.0",
                    "price": "100000.0",
                    "type": "ORDER_TYPE_INSTANT",
                    "side": "ORDER_SIDE_BUY",
                    "crypto_wallet_id": "9",
                    "fiat_wallet_id": "1"
                }
            }
        }
    }
}, description='Returns an order for specified order_id')
def get_order(order_id, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    if int(order_id) < 1 or type(order_id) != int:
        raise HTTPException(status_code=400, detail="invalid_order_id")

    order_message = order_pb2.OrderID(id=order_id)

    try:
        response: order_pb2.OrderDetails = order_stub.GetOrder(order_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id == "":
        logger.info("No order found")
        raise HTTPException(status_code=204)
    else:
        if str(jwt_payload.get("id")) != response.user_id:
            logger.warning("Unauthorized user tried to fetch data")
            raise HTTPException(status_code=401, detail="unauthorized_user_for_method")
        logger.info("Fetched order")
        return MessageToDict(response, preserving_proto_field_name=True)


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
                    "id": "1",
                    "user_id": "1",
                    "date_created": "2024-12-22T11:56:35.387707Z",
                    "date_executed": "1970-01-01T00:00:00Z",
                    "status": "ORDER_STATUS_PENDING",
                    "nominal": "50.0",
                    "price": "100000.0",
                    "type": "ORDER_TYPE_INSTANT",
                    "side": "ORDER_SIDE_BUY",
                    "crypto_wallet_id": "9",
                    "fiat_wallet_id": "1"
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
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id == "":
        logger.error(f"No order with provided id: {order_id}")
        raise HTTPException(status_code=400, detail="operation_failed")
    else:
        logger.info(f"Order with provided id: {order_id} deleted")
        return MessageToDict(response, preserving_proto_field_name=True)


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
                            "id": "1",
                            "user_id": "1",
                            "date_created": "2024-12-22T11:56:35.387707Z",
                            "date_executed": "1970-01-01T00:00:00Z",
                            "status": "ORDER_STATUS_PENDING",
                            "nominal": "50.0",
                            "price": "100000.0",
                            "type": "ORDER_TYPE_INSTANT",
                            "side": "ORDER_SIDE_BUY",
                            "crypto_wallet_id": "9",
                            "fiat_wallet_id": "1"
                        }, {
                            "id": "2",
                            "user_id": "1",
                            "date_created": "2024-12-22T11:56:35.387707Z",
                            "date_executed": "1970-01-01T00:00:00Z",
                            "status": "ORDER_STATUS_PENDING",
                            "nominal": "100.0",
                            "price": "100000.0",
                            "type": "ORDER_TYPE_INSTANT",
                            "side": "ORDER_SIDE_SELL",
                            "crypto_wallet_id": "1",
                            "fiat_wallet_id": "9"
                        }
                    ]}

            }
        }
    }
}, description='Returns orders which fit given filters')
def get_orders(request: Request,
               wallet_id: Optional[str] = "",
               order_status: Optional[OrderStatus] = None,
               order_type: Optional[OrderType] = None,
               side: Optional[OrderSide] = None):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    if wallet_id != "" and int(wallet_id) < 1:
        logger.warning("Incorrect value of wallet_id provided")
        raise HTTPException(status_code=400, detail="wallet_id_invalid")

    mapped_type = transaction_types_mapper[
        order_type.value] if order_type is not None else order_type_pb2.ORDER_TYPE_UNDEFINED
    mapped_side = transaction_side_mapper[side.value] if side is not None else order_side_pb2.ORDER_SIDE_UNDEFINED
    mapped_order_status = transaction_status_mapper[
        order_status.value] if order_status is not None else order_status_pb2.ORDER_STATUS_UNDEFINED

    filter_message = order_pb2.OrderFilter(user_id=jwt_payload.get("id"),
                                           wallet_id=wallet_id,
                                           status=mapped_order_status,
                                           side=mapped_side,
                                           type=mapped_type)

    try:
        response: order_pb2.OrderList = order_stub.GetOrders(filter_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    if len(response.orders) == 0:
        logger.error("No orders found for logged user")
        raise HTTPException(status_code=204)
    else:
        logger.info("Orders found")
        return MessageToDict(response, preserving_proto_field_name=True)
