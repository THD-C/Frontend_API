from fastapi import FastAPI
from src.router import access
import uvicorn

app = FastAPI()

app.include_router(access.router, prefix="/api")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, )