from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserDetail(_message.Message):
    __slots__ = ("id", "name", "surname", "city", "postal_code", "street", "building")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURNAME_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    STREET_FIELD_NUMBER: _ClassVar[int]
    BUILDING_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    surname: str
    city: str
    postal_code: str
    street: str
    building: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., surname: _Optional[str] = ..., city: _Optional[str] = ..., postal_code: _Optional[str] = ..., street: _Optional[str] = ..., building: _Optional[str] = ...) -> None: ...
