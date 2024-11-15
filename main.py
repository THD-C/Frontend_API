from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from src.router import access


app = FastAPI()

app.include_router(access.router, prefix="/api/auth")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, )
