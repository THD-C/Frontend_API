import grpc
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from prometheus_client import start_http_server
from py_grpc_prometheus.prometheus_client_interceptor import PromClientInterceptor
import src.utils.OpenTelemetry.OpenTelemetry as oTEL

from src.utils import DB_MANAGER_PORT, THD_DB_Manager, MONGO_MANAGER_PORT, MONGO_MANAGER, PRICE_MANAGER, \
    PRICE_MANAGER_PORT, ORDERS_SERVICE_PORT, ORDERS_SERVICE
from user import user_pb2_grpc
from wallet import wallet_pb2_grpc
from order import order_pb2_grpc
from payment import payment_pb2_grpc
from secret import secret_pb2_grpc
from password import password_pb2_grpc
from currency import currency_pb2_grpc
from coins import coins_pb2_grpc
from blog import blog_pb2_grpc

from src.utils.logger import logger

GrpcInstrumentorClient().instrument()
prometheus_interceptor = PromClientInterceptor()
start_http_server(8111)

try:

    db_manager_channel = grpc.insecure_channel(f'{THD_DB_Manager}:{DB_MANAGER_PORT}')
    db_manager_channel = grpc.intercept_channel(db_manager_channel, prometheus_interceptor)

    user_stub = user_pb2_grpc.UserStub(db_manager_channel)
    wallet_stub = wallet_pb2_grpc.WalletsStub(db_manager_channel)
    order_stub = order_pb2_grpc.OrderStub(db_manager_channel)
    payment_stub = payment_pb2_grpc.PaymentStub(db_manager_channel)

    mongo_manager_channel = grpc.insecure_channel(f'{MONGO_MANAGER}:{MONGO_MANAGER_PORT}')
    mongo_manager_channel = grpc.intercept_channel(mongo_manager_channel, prometheus_interceptor)

    secret_stub = secret_pb2_grpc.SecretStoreStub(mongo_manager_channel)
    password_stub = password_pb2_grpc.PasswordCheckerStub(mongo_manager_channel)
    currency_stub = currency_pb2_grpc.CurrencyStub(mongo_manager_channel)
    blog_stub = blog_pb2_grpc.BlogStub(mongo_manager_channel)

    price_manager_channel = grpc.insecure_channel(f'{PRICE_MANAGER}:{PRICE_MANAGER_PORT}')
    price_manager_channel = grpc.intercept_channel(price_manager_channel, prometheus_interceptor)

    prices_stub = coins_pb2_grpc.CoinsStub(price_manager_channel)

    orders_service_channel = grpc.insecure_channel(f'{ORDERS_SERVICE}:{ORDERS_SERVICE_PORT}')
    orders_service_channel = grpc.intercept_channel(orders_service_channel)

    orders_service_order_stub = order_pb2_grpc.OrderStub(orders_service_channel)
    orders_service_wallet_stub = wallet_pb2_grpc.WalletsStub(orders_service_channel)

except grpc.RpcError as e:
    logger.error(f"Error occured when connecting to services: {e}")
