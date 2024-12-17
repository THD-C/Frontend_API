from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class PaymentState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAYMENT_STATE_UNKNOWN: _ClassVar[PaymentState]
    PAYMENT_STATE_PENDING: _ClassVar[PaymentState]
    PAYMENT_STATE_ACCEPTED: _ClassVar[PaymentState]
    PAYMENT_STATE_CANCELLED: _ClassVar[PaymentState]
PAYMENT_STATE_UNKNOWN: PaymentState
PAYMENT_STATE_PENDING: PaymentState
PAYMENT_STATE_ACCEPTED: PaymentState
PAYMENT_STATE_CANCELLED: PaymentState
