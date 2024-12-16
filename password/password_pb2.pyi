from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PasswordMessage(_message.Message):
    __slots__ = ("password",)
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    password: str
    def __init__(self, password: _Optional[str] = ...) -> None: ...

class CheckResponse(_message.Message):
    __slots__ = ("isCommon",)
    ISCOMMON_FIELD_NUMBER: _ClassVar[int]
    isCommon: bool
    def __init__(self, isCommon: bool = ...) -> None: ...
