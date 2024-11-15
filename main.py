from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from src.router import access
from src.exceptions.GrpcException import GrpcException

app = FastAPI()

app.include_router(access.router, prefix="/api/auth")


@app.exception_handler(GrpcException)
async def grpc_exception_handler(request, exc: GrpcException):
    return JSONResponse(
        status_code = 500,
        content = {"detail":str(exc)}
    )



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, )
