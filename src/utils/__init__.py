from os import getenv

from src.utils.logger import logger

try:
    DB_MANAGER_PORT = getenv("DB_MANAGER_PORT", default="50051")
    THD_DB_Manager = getenv("DB_MANAGER", default="127.0.0.1")

    MONGO_MANAGER_PORT = getenv("MONGO_MANAGER_PORT", default="50052")
    MONGO_MANAGER = getenv("MONGO_MANAGER", default="127.0.0.1")

    PRICE_MANAGER_PORT = getenv("PRICE_MANAGER_PORT", default="50053")
    PRICE_MANAGER = getenv("PRICE_MANAGER", default="127.0.0.1")
except Exception as e:
    logger.error(f"Error occured when loading environment variables: {e}")
