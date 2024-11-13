from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class OperationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPERATION_TYPE_UNDEFINED: _ClassVar[OperationType]
    OPERATION_TYPE_IN: _ClassVar[OperationType]
    OPERATION_TYPE_OUT: _ClassVar[OperationType]
    OPERATION_TYPE_ORDER_IN: _ClassVar[OperationType]
    OPERATION_TYPE_ORDER_OUT: _ClassVar[OperationType]
OPERATION_TYPE_UNDEFINED: OperationType
OPERATION_TYPE_IN: OperationType
OPERATION_TYPE_OUT: OperationType
OPERATION_TYPE_ORDER_IN: OperationType
OPERATION_TYPE_ORDER_OUT: OperationType
