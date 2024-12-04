from os import getenv

DB_MANAGER_PORT = getenv("DB_MANAGER_PORT", default="50051")
THD_DB_Manager = getenv("DB_MANAGER", default="127.0.0.1")

MONGO_MANAGER_PORT = getenv("MONGO_MANAGER_PORT", default="50052")
MONGO_MANAGER = getenv("MONGO_MANAGER", default="127.0.0.1")
