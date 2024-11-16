from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')

JWT_SECRET_KEY = getenv("JWT_SECRET_KEY", default="crypto_secret_Key")
DB_MANAGER_PORT = getenv("DB_MANAGER_PORT", default="50051")
THD_DB_Manager = getenv("THD_DB_Manager", default="THD_DB_Manager")
GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID")