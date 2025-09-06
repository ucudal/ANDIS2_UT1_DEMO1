import psutil
from utils import get_timestamp

def get_health_status():
    return {
        "timestamp": get_timestamp(),
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "status": "ok"
    }
