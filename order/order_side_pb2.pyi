from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class OrderSide(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_SIDE_UNDEFINED: _ClassVar[OrderSide]
    ORDER_SIDE_BUY: _ClassVar[OrderSide]
    ORDER_SIDE_SELL: _ClassVar[OrderSide]
ORDER_SIDE_UNDEFINED: OrderSide
ORDER_SIDE_BUY: OrderSide
ORDER_SIDE_SELL: OrderSide
