from order import order_status_pb2 as _order_status_pb2
from order import order_type_pb2 as _order_type_pb2
from order import order_side_pb2 as _order_side_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrderDetails(_message.Message):
    __slots__ = ("id", "user_id", "date_created", "date_executed", "status", "nominal", "cash_quantity", "price", "type", "side", "crypto_wallet_id", "fiat_wallet_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DATE_CREATED_FIELD_NUMBER: _ClassVar[int]
    DATE_EXECUTED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NOMINAL_FIELD_NUMBER: _ClassVar[int]
    CASH_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    CRYPTO_WALLET_ID_FIELD_NUMBER: _ClassVar[int]
    FIAT_WALLET_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    date_created: _timestamp_pb2.Timestamp
    date_executed: _timestamp_pb2.Timestamp
    status: _order_status_pb2.OrderStatus
    nominal: str
    cash_quantity: str
    price: str
    type: _order_type_pb2.OrderType
    side: _order_side_pb2.OrderSide
    crypto_wallet_id: str
    fiat_wallet_id: str
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., date_created: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., date_executed: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., status: _Optional[_Union[_order_status_pb2.OrderStatus, str]] = ..., nominal: _Optional[str] = ..., cash_quantity: _Optional[str] = ..., price: _Optional[str] = ..., type: _Optional[_Union[_order_type_pb2.OrderType, str]] = ..., side: _Optional[_Union[_order_side_pb2.OrderSide, str]] = ..., crypto_wallet_id: _Optional[str] = ..., fiat_wallet_id: _Optional[str] = ...) -> None: ...

class OrderID(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UserID(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class OrderList(_message.Message):
    __slots__ = ("orders",)
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    orders: _containers.RepeatedCompositeFieldContainer[OrderDetails]
    def __init__(self, orders: _Optional[_Iterable[_Union[OrderDetails, _Mapping]]] = ...) -> None: ...
