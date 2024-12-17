import os
from dotenv import load_dotenv


load_dotenv()

SERVICE_NAME = "Frontend_API"

TEMPO_HOSTNAME = os.getenv("TEMPO_HOSTNAME", "Tempo")
TEMPO_PORT = os.getenv("TEMPO_PORT", "4317")
