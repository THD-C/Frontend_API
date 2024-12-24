from fastapi import APIRouter


health_check = APIRouter(tags=["HealthCheck"])

@health_check.get("/")
def get_health_check():
    return {"status": "ok"}