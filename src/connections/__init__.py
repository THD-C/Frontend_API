import grpc

from src.utils import DB_MANAGER_PORT, THD_DB_Manager, MONGO_MANAGER_PORT, MONGO_MANAGER
from user import user_pb2_grpc
from wallet import wallet_pb2_grpc
from order import order_pb2_grpc
from payment import payment_pb2_grpc
from secret import secret_pb2_grpc

from src.utils.logger import logger

try:
    db_manager_channel = grpc.insecure_channel(f'{THD_DB_Manager}:{DB_MANAGER_PORT}')
    user_stub = user_pb2_grpc.UserStub(db_manager_channel)
    wallet_stub = wallet_pb2_grpc.WalletsStub(db_manager_channel)
    order_stub = order_pb2_grpc.OrderStub(db_manager_channel)
    payment_stub = payment_pb2_grpc.PaymentStub(db_manager_channel)

    mongo_manager_channel = grpc.insecure_channel(f'{MONGO_MANAGER}:{MONGO_MANAGER_PORT}')
    secret_stub = secret_pb2_grpc.SecretStoreStub(mongo_manager_channel)
except grpc.RpcError as e:
    logger.error(f"Error occured when connecting to services: {e}")