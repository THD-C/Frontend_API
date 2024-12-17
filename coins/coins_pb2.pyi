from order import order_status_pb2 as _order_status_pb2
from order import order_type_pb2 as _order_type_pb2
from order import order_side_pb2 as _order_side_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CoinId(_message.Message):
    __slots__ = ("coin_id",)
    COIN_ID_FIELD_NUMBER: _ClassVar[int]
    coin_id: str
    def __init__(self, coin_id: _Optional[str] = ...) -> None: ...

class CoinData(_message.Message):
    __slots__ = ("coin_id", "coin_data")
    COIN_ID_FIELD_NUMBER: _ClassVar[int]
    COIN_DATA_FIELD_NUMBER: _ClassVar[int]
    coin_id: str
    coin_data: str
    def __init__(self, coin_id: _Optional[str] = ..., coin_data: _Optional[str] = ...) -> None: ...
