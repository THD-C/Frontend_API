import grpc

from src.utils import DB_MANAGER_PORT

channel = grpc.insecure_channel(f'localhost:{DB_MANAGER_PORT}')