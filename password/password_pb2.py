# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: password/password.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'password/password.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17password/password.proto\x12\x08password\"#\n\x0fPasswordMessage\x12\x10\n\x08password\x18\x01 \x01(\t\"!\n\rCheckResponse\x12\x10\n\x08isCommon\x18\x01 \x01(\x08\x32V\n\x0fPasswordChecker\x12\x43\n\rCheckPassword\x12\x19.password.PasswordMessage\x1a\x17.password.CheckResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'password.password_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PASSWORDMESSAGE']._serialized_start=37
  _globals['_PASSWORDMESSAGE']._serialized_end=72
  _globals['_CHECKRESPONSE']._serialized_start=74
  _globals['_CHECKRESPONSE']._serialized_end=107
  _globals['_PASSWORDCHECKER']._serialized_start=109
  _globals['_PASSWORDCHECKER']._serialized_end=195
# @@protoc_insertion_point(module_scope)
