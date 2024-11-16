import grpc

from src.utils import DB_MANAGER_PORT, THD_DB_Manager

channel = grpc.insecure_channel(f'{THD_DB_Manager}:{DB_MANAGER_PORT}')