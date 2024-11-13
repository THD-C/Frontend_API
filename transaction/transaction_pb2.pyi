from transaction import operation_type_pb2 as _operation_type_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Transaction(_message.Message):
    __slots__ = ("id", "date", "operation_type", "nominal_value")
    ID_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    NOMINAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    id: str
    date: _timestamp_pb2.Timestamp
    operation_type: _operation_type_pb2.OperationType
    nominal_value: str
    def __init__(self, id: _Optional[str] = ..., date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., operation_type: _Optional[_Union[_operation_type_pb2.OperationType, str]] = ..., nominal_value: _Optional[str] = ...) -> None: ...
