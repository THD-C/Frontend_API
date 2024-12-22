from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CoinDataRequest(_message.Message):
    __slots__ = ("coin_id",)
    COIN_ID_FIELD_NUMBER: _ClassVar[int]
    coin_id: str
    def __init__(self, coin_id: _Optional[str] = ...) -> None: ...

class HistoricalDataRequest(_message.Message):
    __slots__ = ("coin_id", "start_date", "end_date")
    COIN_ID_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    coin_id: str
    start_date: str
    end_date: str
    def __init__(self, coin_id: _Optional[str] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ...) -> None: ...

class DataResponse(_message.Message):
    __slots__ = ("status", "error_message", "data")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    status: str
    error_message: str
    data: str
    def __init__(self, status: _Optional[str] = ..., error_message: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...
