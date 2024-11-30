from datetime import datetime, UTC

from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter, HTTPException, Request
from grpc import RpcError
from pydantic import BaseModel

from src.connections import channel
from user import user_detail_pb2
from order import order_pb2, order_type_pb2, order_status_pb2, order_side_pb2, order_pb2_grpc
from src.utils.auth import verify_user


class OrderDetails(BaseModel):
    user_id: str
    currency: str
    currency_used: str
    nominal: str
    cash_quantity: str
    price: str
    type: str
    side: str


transaction_types_mapper = {
    "UNDEFINED": order_type_pb2.OrderType.UNDEFINED,
    "STOP_LOSS": order_type_pb2.OrderType.STOP_LOSS,
    "TAKE_PROFIT": order_type_pb2.OrderType.ORDER_TYPE_TAKE_PROFIT,
    "INSTANT": order_type_pb2.OrderType.ORDER_TYPE_INSTANT
}

transaction_side_mapper = {
    "UNDEFINED": order_side_pb2.ORDER_SIDE_UNDEFINED,
    "BUY": order_side_pb2.ORDER_SIDE_BUY,
    "SELL": order_side_pb2.ORDER_SIDE_SELL
}

orders = APIRouter(tags=["Orders"])


@orders.post("/", responses={
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
}, description='Creates an order for specifiec currency')
def create_wallet(orderDetails: OrderDetails, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)
    if str(jwt_payload.get("id")) != orderDetails.user_id:
        raise HTTPException(status_code=401, detail="unauthorized_user_for_method")

    order_type_order_details = transaction_types_mapper.get(orderDetails.orderType)
    order_side_order_details = transaction_side_mapper.get(orderDetails.side)
    if order_type_order_details or order_side_order_details is None:
        raise HTTPException(status_code=400, detail="operation_failed")

    orderRequest = order_pb2.OrderDetails(user_id = orderDetails.user_id,
                                          date_created=datetime.now(UTC),
                                          date_executed=datetime(1970, 1, 1, tzinfo=UTC),
                                          status=order_status_pb2.ORDER_STATUS_UNDEFINED,
                                          currency=orderDetails.currency,
                                          nominal=orderDetails.nominal,
                                          cash_quantity=orderDetails.cash_quantity,
                                          price=orderDetails.price,
                                          type=order_type_order_details,
                                          side=order_side_order_details,
                                          currency_used=orderDetails.currency_used
                                          )

    try:
        stub = order_pb2_grpc.OrderStub(channel)
        response: order_pb2.OrderDetails = stub.CreateOrder(orderRequest)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id != "":
        return MessageToDict(response)

    raise HTTPException(status_code=400, detail="operation_failed")

@orders.get("/")
def get_order(order_id, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    order_message = order_pb2.OrderID(id = order_id)

    try:
        stub = order_pb2_grpc.OrderStub(channel)
        response: order_pb2.OrderDetails = stub.GetOrder(order_message)
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

@orders.delete("/")
def delete_order(order_id, request: Request):
    get_order(order_id, request=request)

    delete_order_message = order_pb2.OrderID(id = order_id)

    try:
        stub = order_pb2_grpc.OrderStub(channel)
        response: order_pb2.OrderDetails = stub.DeleteOrder(delete_order_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if response.id == "":
        raise HTTPException(status_code=400, detail="operation_failed")
    else:
        return MessageToDict(response)

@orders.get("/orders")
def get_orders(user_id, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)
    if str(jwt_payload.get("id")) != user_id:
        raise HTTPException(status_code=401, detail="unauthorized_user_for_method")

    user_message = order_pb2.UserID(id = user_id)

    try:
        stub = order_pb2_grpc.OrderStub(channel)
        response: order_pb2.OrderList = stub.GetOrderList(user_message)
    except RpcError as e:
        print("gRPC error details:", e.details())
        print("gRPC status code:", e.code())
        raise HTTPException(status_code=500, detail="internal_server_error")

    if len(response.orders) == 0:
        raise HTTPException(status_code=204)
    else:
        return MessageToDict(response)