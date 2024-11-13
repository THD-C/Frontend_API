from fastapi import FastAPI

from src.connections.connections import open_db_manager_connection

db_channel = open_db_manager_connection()

app = FastAPI()

@app.get("/")
async def root():
    return {f'Hello World" + {12}'}

