# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: coins/coins.proto
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
    'coins/coins.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from order import order_status_pb2 as order_dot_order__status__pb2
from order import order_type_pb2 as order_dot_order__type__pb2
from order import order_side_pb2 as order_dot_order__side__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x63oins/coins.proto\x12\x05order\x1a\x18order/order_status.proto\x1a\x16order/order_type.proto\x1a\x16order/order_side.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x19\n\x06\x43oinId\x12\x0f\n\x07\x63oin_id\x18\x01 \x01(\t\".\n\x08\x43oinData\x12\x0f\n\x07\x63oin_id\x18\x01 \x01(\t\x12\x11\n\tcoin_data\x18\x02 \x01(\t26\n\x05\x43oins\x12-\n\x0bGetCoinData\x12\r.order.CoinId\x1a\x0f.order.CoinDatab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'coins.coins_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_COINID']._serialized_start=135
  _globals['_COINID']._serialized_end=160
  _globals['_COINDATA']._serialized_start=162
  _globals['_COINDATA']._serialized_end=208
  _globals['_COINS']._serialized_start=210
  _globals['_COINS']._serialized_end=264
# @@protoc_insertion_point(module_scope)
