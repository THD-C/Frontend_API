from os import getenv

DB_MANAGER_PORT = getenv("DB_MANAGER_PORT", default="50051")
THD_DB_Manager = getenv("DB_Manager", default="THD_DB_Manager")

MONGO_MANAGER_PORT = getenv("MONGO_MANAGER_PORT", default="50051")
MONGO_MANAGER = getenv("MONGO_MANAGER", default="THD_Mongo_Manager")
