# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: wallet/wallet.proto
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
    'wallet/wallet.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13wallet/wallet.proto\x12\x06wallet\"Y\n\x06Wallet\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08\x63urrency\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\x12\x0f\n\x07user_id\x18\x04 \x01(\t\x12\x11\n\tis_crypto\x18\x05 \x01(\x08\"-\n\nWalletList\x12\x1f\n\x07wallets\x18\x01 \x03(\x0b\x32\x0e.wallet.Wallet\"\x14\n\x06UserID\x12\n\n\x02id\x18\x01 \x01(\t\"\x16\n\x08WalletID\x12\n\n\x02id\x18\x01 \x01(\t2\x81\x02\n\x07Wallets\x12.\n\x0c\x43reateWallet\x12\x0e.wallet.Wallet\x1a\x0e.wallet.Wallet\x12.\n\x0cUpdateWallet\x12\x0e.wallet.Wallet\x1a\x0e.wallet.Wallet\x12\x30\n\x0c\x44\x65leteWallet\x12\x10.wallet.WalletID\x1a\x0e.wallet.Wallet\x12-\n\tGetWallet\x12\x10.wallet.WalletID\x1a\x0e.wallet.Wallet\x12\x35\n\x0fGetUsersWallets\x12\x0e.wallet.UserID\x1a\x12.wallet.WalletListb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'wallet.wallet_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_WALLET']._serialized_start=31
  _globals['_WALLET']._serialized_end=120
  _globals['_WALLETLIST']._serialized_start=122
  _globals['_WALLETLIST']._serialized_end=167
  _globals['_USERID']._serialized_start=169
  _globals['_USERID']._serialized_end=189
  _globals['_WALLETID']._serialized_start=191
  _globals['_WALLETID']._serialized_end=213
  _globals['_WALLETS']._serialized_start=216
  _globals['_WALLETS']._serialized_end=473
# @@protoc_insertion_point(module_scope)
