from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ChangePass(_message.Message):
    __slots__ = ("login", "old_password", "new_password")
    LOGIN_FIELD_NUMBER: _ClassVar[int]
    OLD_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    NEW_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    login: str
    old_password: str
    new_password: str
    def __init__(self, login: _Optional[str] = ..., old_password: _Optional[str] = ..., new_password: _Optional[str] = ...) -> None: ...

class RegUser(_message.Message):
    __slots__ = ("username", "email", "password", "name", "surname", "street", "building", "city", "postal_code", "country")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURNAME_FIELD_NUMBER: _ClassVar[int]
    STREET_FIELD_NUMBER: _ClassVar[int]
    BUILDING_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    username: str
    email: str
    password: str
    name: str
    surname: str
    street: str
    building: str
    city: str
    postal_code: str
    country: str
    def __init__(self, username: _Optional[str] = ..., email: _Optional[str] = ..., password: _Optional[str] = ..., name: _Optional[str] = ..., surname: _Optional[str] = ..., street: _Optional[str] = ..., building: _Optional[str] = ..., city: _Optional[str] = ..., postal_code: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...

class AuthUser(_message.Message):
    __slots__ = ("login", "password")
    LOGIN_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    login: str
    password: str
    def __init__(self, login: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class AuthResponse(_message.Message):
    __slots__ = ("success", "id", "email", "username")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    success: bool
    id: str
    email: str
    username: str
    def __init__(self, success: bool = ..., id: _Optional[str] = ..., email: _Optional[str] = ..., username: _Optional[str] = ...) -> None: ...

class RegResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class ReqUpdateUser(_message.Message):
    __slots__ = ("id", "email", "password", "name", "surname", "street", "building", "city", "postal_code", "country")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURNAME_FIELD_NUMBER: _ClassVar[int]
    STREET_FIELD_NUMBER: _ClassVar[int]
    BUILDING_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    password: str
    name: str
    surname: str
    street: str
    building: str
    city: str
    postal_code: str
    country: str
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., password: _Optional[str] = ..., name: _Optional[str] = ..., surname: _Optional[str] = ..., street: _Optional[str] = ..., building: _Optional[str] = ..., city: _Optional[str] = ..., postal_code: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...

class ResultResponse(_message.Message):
    __slots__ = ("success", "id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    id: str
    def __init__(self, success: bool = ..., id: _Optional[str] = ...) -> None: ...

class ReqDeleteUser(_message.Message):
    __slots__ = ("id", "mail", "password")
    ID_FIELD_NUMBER: _ClassVar[int]
    MAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    id: str
    mail: str
    password: str
    def __init__(self, id: _Optional[str] = ..., mail: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class ReqGetUserDetails(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class UserDetails(_message.Message):
    __slots__ = ("username", "email", "name", "surname", "street", "building", "city", "postal_code", "country")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURNAME_FIELD_NUMBER: _ClassVar[int]
    STREET_FIELD_NUMBER: _ClassVar[int]
    BUILDING_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    POSTAL_CODE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    username: str
    email: str
    name: str
    surname: str
    street: str
    building: str
    city: str
    postal_code: str
    country: str
    def __init__(self, username: _Optional[str] = ..., email: _Optional[str] = ..., name: _Optional[str] = ..., surname: _Optional[str] = ..., street: _Optional[str] = ..., building: _Optional[str] = ..., city: _Optional[str] = ..., postal_code: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...
