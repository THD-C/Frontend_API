# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from transaction import transaction_pb2 as transaction_dot_transaction__pb2

GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in transaction/transaction_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class TransactionStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateTransaction = channel.unary_unary(
                '/transaction.Transaction/CreateTransaction',
                request_serializer=transaction_dot_transaction__pb2.TransactionDetails.SerializeToString,
                response_deserializer=transaction_dot_transaction__pb2.TransactionDetails.FromString,
                _registered_method=True)
        self.DeleteTransaction = channel.unary_unary(
                '/transaction.Transaction/DeleteTransaction',
                request_serializer=transaction_dot_transaction__pb2.TransactionID.SerializeToString,
                response_deserializer=transaction_dot_transaction__pb2.TransactionDetails.FromString,
                _registered_method=True)
        self.UpdateTransaction = channel.unary_unary(
                '/transaction.Transaction/UpdateTransaction',
                request_serializer=transaction_dot_transaction__pb2.TransactionDetails.SerializeToString,
                response_deserializer=transaction_dot_transaction__pb2.TransactionDetails.FromString,
                _registered_method=True)
        self.GetTransaction = channel.unary_unary(
                '/transaction.Transaction/GetTransaction',
                request_serializer=transaction_dot_transaction__pb2.TransactionID.SerializeToString,
                response_deserializer=transaction_dot_transaction__pb2.TransactionDetails.FromString,
                _registered_method=True)
        self.GetTransactionList = channel.unary_unary(
                '/transaction.Transaction/GetTransactionList',
                request_serializer=transaction_dot_transaction__pb2.WalletID.SerializeToString,
                response_deserializer=transaction_dot_transaction__pb2.TransactionList.FromString,
                _registered_method=True)


class TransactionServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateTransaction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTransaction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateTransaction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTransaction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTransactionList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TransactionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateTransaction,
                    request_deserializer=transaction_dot_transaction__pb2.TransactionDetails.FromString,
                    response_serializer=transaction_dot_transaction__pb2.TransactionDetails.SerializeToString,
            ),
            'DeleteTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteTransaction,
                    request_deserializer=transaction_dot_transaction__pb2.TransactionID.FromString,
                    response_serializer=transaction_dot_transaction__pb2.TransactionDetails.SerializeToString,
            ),
            'UpdateTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateTransaction,
                    request_deserializer=transaction_dot_transaction__pb2.TransactionDetails.FromString,
                    response_serializer=transaction_dot_transaction__pb2.TransactionDetails.SerializeToString,
            ),
            'GetTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTransaction,
                    request_deserializer=transaction_dot_transaction__pb2.TransactionID.FromString,
                    response_serializer=transaction_dot_transaction__pb2.TransactionDetails.SerializeToString,
            ),
            'GetTransactionList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTransactionList,
                    request_deserializer=transaction_dot_transaction__pb2.WalletID.FromString,
                    response_serializer=transaction_dot_transaction__pb2.TransactionList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'transaction.Transaction', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('transaction.Transaction', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Transaction(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateTransaction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/transaction.Transaction/CreateTransaction',
            transaction_dot_transaction__pb2.TransactionDetails.SerializeToString,
            transaction_dot_transaction__pb2.TransactionDetails.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteTransaction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/transaction.Transaction/DeleteTransaction',
            transaction_dot_transaction__pb2.TransactionID.SerializeToString,
            transaction_dot_transaction__pb2.TransactionDetails.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateTransaction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/transaction.Transaction/UpdateTransaction',
            transaction_dot_transaction__pb2.TransactionDetails.SerializeToString,
            transaction_dot_transaction__pb2.TransactionDetails.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetTransaction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/transaction.Transaction/GetTransaction',
            transaction_dot_transaction__pb2.TransactionID.SerializeToString,
            transaction_dot_transaction__pb2.TransactionDetails.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetTransactionList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/transaction.Transaction/GetTransactionList',
            transaction_dot_transaction__pb2.WalletID.SerializeToString,
            transaction_dot_transaction__pb2.TransactionList.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
