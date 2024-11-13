from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class OrderType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_TYPE_UNDEFINED: _ClassVar[OrderType]
    ORDER_TYPE_STOP_LOSS: _ClassVar[OrderType]
    ORDER_TYPE_TAKE_PROFIT: _ClassVar[OrderType]
    ORDER_TYPE_INSTANT: _ClassVar[OrderType]
ORDER_TYPE_UNDEFINED: OrderType
ORDER_TYPE_STOP_LOSS: OrderType
ORDER_TYPE_TAKE_PROFIT: OrderType
ORDER_TYPE_INSTANT: OrderType
