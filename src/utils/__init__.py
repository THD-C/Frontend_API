from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')

JWT_SECRET_KEY = getenv("JWT_SECRET_KEY", default="crypto_secret_Key")
DB_MANAGER_PORT = getenv("DB_MANAGER_PORT", default="50051")