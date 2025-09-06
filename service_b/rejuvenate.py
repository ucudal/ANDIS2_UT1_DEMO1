import time
import logging

def start_rejuvenate(logger):
    if logger is None:
        logger = logging.getLogger("uvicorn")
    while True:
        logger.info("Rejuvenecimiento: limpieza de recursos")
        # Aquí podrías limpiar recursos, cerrar conexiones, etc.
        time.sleep(60)
