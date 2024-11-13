from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class OrderStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_STATUS_UNDEFINED: _ClassVar[OrderStatus]
    ORDER_STATUS_ACCEPTED: _ClassVar[OrderStatus]
    ORDER_STATUS_REJECTED: _ClassVar[OrderStatus]
    ORDER_STATUS_PENDING: _ClassVar[OrderStatus]
    ORDER_STATUS_PARTIALLY_COMPLETED: _ClassVar[OrderStatus]
    ORDER_STATUS_COMPLETED: _ClassVar[OrderStatus]
    ORDER_STATUS_CANCELLED: _ClassVar[OrderStatus]
    ORDER_STATUS_EXPIRED: _ClassVar[OrderStatus]
    ORDER_STATUS_IN_PROGRESS: _ClassVar[OrderStatus]
ORDER_STATUS_UNDEFINED: OrderStatus
ORDER_STATUS_ACCEPTED: OrderStatus
ORDER_STATUS_REJECTED: OrderStatus
ORDER_STATUS_PENDING: OrderStatus
ORDER_STATUS_PARTIALLY_COMPLETED: OrderStatus
ORDER_STATUS_COMPLETED: OrderStatus
ORDER_STATUS_CANCELLED: OrderStatus
ORDER_STATUS_EXPIRED: OrderStatus
ORDER_STATUS_IN_PROGRESS: OrderStatus
