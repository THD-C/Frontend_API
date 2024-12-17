from payment import payment_state_pb2 as _payment_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PaymentDetails(_message.Message):
    __slots__ = ("id", "user_id", "currency", "nominal", "state")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    NOMINAL_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    currency: str
    nominal: str
    state: _payment_state_pb2.PaymentState
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., currency: _Optional[str] = ..., nominal: _Optional[str] = ..., state: _Optional[_Union[_payment_state_pb2.PaymentState, str]] = ...) -> None: ...

class UserID(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class PaymentID(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class PaymentList(_message.Message):
    __slots__ = ("payments",)
    PAYMENTS_FIELD_NUMBER: _ClassVar[int]
    payments: _containers.RepeatedCompositeFieldContainer[PaymentDetails]
    def __init__(self, payments: _Optional[_Iterable[_Union[PaymentDetails, _Mapping]]] = ...) -> None: ...

class UnpaidSessions(_message.Message):
    __slots__ = ("unpaid",)
    UNPAID_FIELD_NUMBER: _ClassVar[int]
    unpaid: bool
    def __init__(self, unpaid: bool = ...) -> None: ...
