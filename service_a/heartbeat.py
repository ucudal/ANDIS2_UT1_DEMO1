import httpx
import logging
import time

def start_heartbeat(url, logger=None):
    while True:
        try:
            r = httpx.get(url, timeout=2)
            logger.info(f"Heartbeat from service at {url} is health {r.json()}")
        except Exception as e:
            logger.error(f"Heartbeat from service at {url} failed: {e}")
        time.sleep(5)
