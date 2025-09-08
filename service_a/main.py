import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import threading
import os
import debugpy
import logging

from utils import retry_request, sanity_check, get_timestamp
from health import get_health_status
from heartbeat import start_heartbeat
from shadow import shadow_test

logger = None
last_probs = []
current_prob = 1.0

LOG_FILE=os.environ.get("LOG_FILE", "service_a.log")
SERVICE_B_URL=os.environ.get("SERVICE_B_URL", "http://localhost:8002")
SHADOW_B_URL=os.environ.get("SHADOW_B_URL", "http://localhost:8003")  # Para shadowing, si se usa
NODE_NAME = os.environ.get("NODE_NAME", "service_a")
NODE_PORT = int(os.environ.get("NODE_PORT", "8001"))

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
    threading.Thread(target=lambda: start_heartbeat(
        f"{SERVICE_B_URL}/health", logger=logger), daemon=True).start()

    shadow_test(f"{SHADOW_B_URL}/health", logger=logger)

    yield  # This is where the app runs

    # Shutdown
    logger.info(f"App {NODE_NAME} shutting down")

app = FastAPI(
    title="Service A - API Principal",
    description="Servicio principal que consume Service B y aplica tácticas de disponibilidad.",
    lifespan=lifespan
)

class SaludoResponse(BaseModel):
    saludo: str
    timestamp: str = None
    error: str = None

class HealthResponse(BaseModel):
    timestamp: str
    cpu_percent: float
    memory_percent: float
    status: str

class ConfigRequest(BaseModel):
    prob: float

class ShadowRequest(BaseModel):
    enable: bool

@app.get(
    "/ping",
    tags=["Ping/Echo"],
    summary="Ping al servicio",
    response_model=dict,
    description="Endpoint para verificar la disponibilidad del servicio. Responde con 'pong' y un timestamp."
)
async def ping():
    logger.info("Ping received")
    return {"pong": True, "timestamp": get_timestamp()}

@app.get(
    "/health",
    tags=["Healthcheck"],
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
    summary="Obtener saludo desde Service B",
    response_model=SaludoResponse,
    description="Obtiene un saludo desde Service B. Si Service B falla, responde con un mensaje degradado."
)
async def saludo():
    global logger
    try:
        sanity_check(SERVICE_B_URL)
        response = retry_request(f"{SERVICE_B_URL}/saludo", logger=logger)
        logger.info(f"Saludo response: {response}")
        return response
    except Exception as e:
        logger.info(f"Error in /saludo: {e}")
        return JSONResponse(content={"saludo": "Servicio degradado", "error": str(e)}, status_code=503)

@app.post(
    "/config",
    summary="Configurar probabilidad de disponibilidad en Service B",
    response_model=dict,
    description="Permite configurar la probabilidad de disponibilidad en Service B. Valor entre 0 y 1.",
)
async def set_config(config: ConfigRequest = Body(..., example={"prob": 0.8})):
    global last_probs, current_prob, logger
    prob = config.prob
    if not (0 <= prob <= 1):
        logger.info(f"Sanity check failed: prob={prob}")
        raise HTTPException(status_code=400, detail="Probabilidad fuera de rango")
    try:
        last_probs.append(current_prob)
        current_prob = prob
        response = retry_request(f"{SERVICE_B_URL}/config", method="POST", json={"prob": current_prob}, logger=logger)
        logger.info(f"Config set: {current_prob}")
        return response
    except Exception as e:
        logger.info(f"Error setting config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/rollback",
    summary="Revertir probabilidad de disponibilidad en Service B",
    response_model=dict,
    description="Revierte la probabilidad de disponibilidad en Service B al valor anterior."
)
async def rollback():
    global last_probs, current_prob, logger
    try:
        if last_probs:
            current_prob = last_probs.pop()
        else:
            current_prob = 1.0  # Valor por defecto si no hay historial

        response = retry_request(f"{SERVICE_B_URL}/config", method="POST", json={"prob": current_prob}, logger=logger)
        logger.info(f"Rollback to prob={current_prob}")
        return response
    except Exception as e:
        logger.info(f"Error in rollback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/shadow",
    summary="Activar/desactivar modo shadow",
    response_model=dict,
    description="Activa o desactiva el modo shadow para probar Service B alternativo."
)
async def enable_shadow(shadow: ShadowRequest = Body(..., example={"enable": True})):
    global shadow_mode
    shadow_mode = shadow.enable
    logger.info(f"Shadow mode set to {shadow_mode}")
    return {"shadow_mode": shadow_mode}

if __name__ == "__main__":
    debugpy.listen(("0.0.0.0", 5678))
    uvicorn.run("main:app", host="0.0.0.0", port= NODE_PORT)
