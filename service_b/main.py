import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import random
import threading
import os
import debugpy
import logging

from utils import get_timestamp
from health import get_health_status
from rejuvenate import start_rejuvenate

prob = 1.0  # Probabilidad inicial de disponibilidad
logger = None

LOG_FILE=os.environ.get("LOG_FILE", "service_b.log")
NODE_NAME = os.environ.get("NODE_NAME", "service_b")
NODE_PORT = int(os.environ.get("NODE_PORT", "8002"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    os.makedirs('/app/logs', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"/app/logs/{LOG_FILE}"),
            logging.StreamHandler()
        ]
    )
    global logger
    logger = logging.getLogger("uvicorn")
    logger.info(f"Service {NODE_NAME} starting up at {NODE_PORT}")
    logger.info(f"Debugger for {NODE_NAME} listening on port 5678...")
    threading.Thread(target=lambda: start_rejuvenate(logger=logger), daemon=True).start()

    yield  # This is where the app runs

    # Shutdown
    logger.info(f"App {NODE_NAME} shutting down")

app = FastAPI(
    title="Service B - Backend",
    description="Servicio backend que responde a saludos y simula fallas configurables.",
    lifespan=lifespan
)

class SaludoResponse(BaseModel):
    saludo: str
    timestamp: str = None

class HealthResponse(BaseModel):
    timestamp: str
    cpu_percent: float
    memory_percent: float
    status: str

class ConfigRequest(BaseModel):
    prob: float

@app.get(
    "/ping",
    tags=["Disponibilidad", "Ping/Echo"],
    summary="Ping al servicio",
    response_model=dict,
    description="Endpoint para verificar la disponibilidad del servicio. Responde con 'pong' y un timestamp."
)
async def ping():
    logger.info("Ping received")
    return {"pong": True, "timestamp": get_timestamp()}

@app.get(
    "/health",
    tags=["Monitoreo", "Healthcheck"],
    summary="Estado de salud del servicio",
    response_model=HealthResponse,
    description="Devuelve el estado de salud del servicio, incluyendo uso de CPU y memoria."
)
async def health():
    status = get_health_status()
    logger.info(f"Health check: {status}")
    return status

@app.get(
    "/saludo",
    tags=["Saludo", "Simulación de fallas"],
    summary="Obtener saludo",
    response_model=SaludoResponse,
    description="Devuelve un saludo si el servicio está disponible según la probabilidad configurada."
)
async def saludo():
    global prob
    if random.random() < prob:
        logger.info("Saludo OK")
        return {"saludo": "Hola desde Service B", "timestamp": get_timestamp()}
    else:
        logger.info("Saludo ERROR")
        raise HTTPException(status_code=503, detail="Service B no disponible")

@app.post(
    "/config",
    tags=["Configuración"],
    summary="Configurar probabilidad de disponibilidad",
    response_model=dict,
    description="Permite configurar la probabilidad de disponibilidad del servicio. Valor entre 0 y 1.",
)
async def set_config(config: ConfigRequest = Body(..., example={"prob": 0.8})):
    new_prob = config.prob
    if not isinstance(new_prob, float) or not (0 <= new_prob <= 1):
        logger.info(f"Sanity check failed: prob={new_prob}")
        raise HTTPException(status_code=400, detail="Probabilidad fuera de rango")
    global prob
    prob = new_prob
    logger.info(f"Probabilidad de disponibilidad actualizada a {prob}")
    return {"prob": prob}

if __name__ == "__main__":
    debugpy.listen(("0.0.0.0", 5678))
    uvicorn.run("main:app", host="0.0.0.0", port=NODE_PORT)
