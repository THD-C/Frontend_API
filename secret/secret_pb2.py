# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: secret/secret.proto
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
    'secret/secret.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13secret/secret.proto\x12\x06secret\"\x1a\n\nSecretName\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1c\n\x0bSecretValue\x12\r\n\x05value\x18\x01 \x01(\t2C\n\x0bSecretStore\x12\x34\n\tGetSecret\x12\x12.secret.SecretName\x1a\x13.secret.SecretValueb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'secret.secret_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SECRETNAME']._serialized_start=31
  _globals['_SECRETNAME']._serialized_end=57
  _globals['_SECRETVALUE']._serialized_start=59
  _globals['_SECRETVALUE']._serialized_end=87
  _globals['_SECRETSTORE']._serialized_start=89
  _globals['_SECRETSTORE']._serialized_end=156
# @@protoc_insertion_point(module_scope)
