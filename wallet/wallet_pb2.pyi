from user import user_detail_pb2 as _user_detail_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Wallet(_message.Message):
    __slots__ = ("id", "currency", "value", "user_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    currency: str
    value: str
    user_id: str
    def __init__(self, id: _Optional[str] = ..., currency: _Optional[str] = ..., value: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class WalletList(_message.Message):
    __slots__ = ("wallets",)
    WALLETS_FIELD_NUMBER: _ClassVar[int]
    wallets: _containers.RepeatedCompositeFieldContainer[Wallet]
    def __init__(self, wallets: _Optional[_Iterable[_Union[Wallet, _Mapping]]] = ...) -> None: ...
