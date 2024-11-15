from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.router import access


app = FastAPI()

origins = [
    "Localhost",
    "Localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(access.router, prefix="/api/auth")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, )
