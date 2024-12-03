import grpc

from secret import secret_pb2_grpc

from src.utils import DB_MANAGER_PORT, THD_DB_Manager, MONGO_MANAGER_PORT, MONGO_MANAGER
from user import user_pb2_grpc
from wallet import wallet_pb2_grpc

db_manager_channel = grpc.insecure_channel(f'{THD_DB_Manager}:{DB_MANAGER_PORT}')
user_stub = user_pb2_grpc.UserStub(db_manager_channel)
wallet_stub = wallet_pb2_grpc.WalletsStub(db_manager_channel)

mongo_manager_channel = grpc.insecure_channel(f'{MONGO_MANAGER}:{MONGO_MANAGER_PORT}')
secret_stub = secret_pb2_grpc.SecretStoreStub(mongo_manager_channel)