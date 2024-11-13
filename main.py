from fastapi import FastAPI
from src.router import access
import uvicorn

from src.connections.connections import open_db_manager_connection

#db_channel = open_db_manager_connection()

app = FastAPI()

app.include_router(access.router)


@app.get("/")
async def root():
    return {f'Hello World" + {12}'}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)