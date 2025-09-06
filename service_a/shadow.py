import logging
import httpx

def shadow_test(url, logger=None):
    if logger is None:
        logger = logging.getLogger("uvicorn")
    try:
        r = httpx.get(url, timeout=2)
        logger.info(f"Shadowing test: Shadow B health {r.json()}")
    except Exception as e:
        logger.info(f"Shadowing test failed: {e}")
