from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.router import access, wallets, user


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200"
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
