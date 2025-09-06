# main.py
from fastapi import FastAPI, HTTPException, Body
import random

app = FastAPI(
    title="API de demo",
    description="API para simular disponibilidad de una aplicación y ajustar el uptime.",
    version="1.0"
)

# Variable global para el uptime
uptime_value = 1

@app.get(
    "/saludo",
    summary="Obtener saludo si el sistema está disponible",
    description="Devuelve un mensaje de saludo si el sistema está disponible según el uptime configurado. Si no, retorna un error 503.",
    response_description="Mensaje de saludo o error de servicio no disponible"
)
def saludo():
    if random.random() < uptime_value:
        return {"mensaje": "¡Hola, el sistema está disponible!"}
    else:
        raise HTTPException(status_code=503, detail="Servicio no disponible temporalmente")

@app.post(
    "/set-uptime",
    summary="Ajustar el valor de uptime del sistema",
    description="Permite establecer el valor de uptime (entre 0 y 1) que determina la probabilidad de que el sistema esté disponible.",
    response_description="Mensaje de confirmación o error de validación"
)
@app.post("/set-uptime")
def set_uptime(value: float = Body(..., embed=True)):
    global uptime_value
    if not (0 <= value <= 1):
        raise HTTPException(status_code=400, detail="El valor de uptime debe estar entre 0 y 1")
    uptime_value = value
    return {"mensaje": f"Uptime actualizado a {uptime_value}"}