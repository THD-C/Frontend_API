from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.models import SecurityScheme
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn

from src.router import access, wallets, user, order, payments
from src.utils.logger import logger
from src.utils.payment_scheduler import setup_payments_scheduler

security = HTTPBearer()
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="THD(C) API",
        version="1.0.0",
        description="API for THD(C) app communicating with presentation layer of the system",
        routes=app.routes,
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

        # Dodajemy security schemes do istniejących komponentów
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }


    openapi_schema["security"] = [
        {
            "BearerAuth": []
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI()

app.openapi = custom_openapi

origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://thdc",
    "http://thdc.tail8ec47f.ts.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(access.access, prefix="/api/auth")
app.include_router(wallets.wallets, prefix="/api/wallets")
app.include_router(user.user, prefix="/api/user")
app.include_router(order.order, prefix="/api/order")
app.include_router(payments.payments, prefix="/api/payments")


if __name__ == "__main__":
    logger.info("Setting up payments scheduler")
    setup_payments_scheduler()
    logger.info("Scheduler started")

    logger.info("Server starting...")
    uvicorn.run(app, host="0.0.0.0", port=8000)