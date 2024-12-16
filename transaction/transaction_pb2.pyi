from transaction import operation_type_pb2 as _operation_type_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TransactionDetails(_message.Message):
    __slots__ = ("id", "date", "nominal_value", "operation_type", "wallet_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    NOMINAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    WALLET_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    date: _timestamp_pb2.Timestamp
    nominal_value: str
    operation_type: _operation_type_pb2.OperationType
    wallet_id: str
    def __init__(self, id: _Optional[str] = ..., date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., nominal_value: _Optional[str] = ..., operation_type: _Optional[_Union[_operation_type_pb2.OperationType, str]] = ..., wallet_id: _Optional[str] = ...) -> None: ...

class TransactionID(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class WalletID(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TransactionList(_message.Message):
    __slots__ = ("transactions",)
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    transactions: _containers.RepeatedCompositeFieldContainer[TransactionDetails]
    def __init__(self, transactions: _Optional[_Iterable[_Union[TransactionDetails, _Mapping]]] = ...) -> None: ...
