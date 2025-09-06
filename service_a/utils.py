import time

def get_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def retry_request(url, method="GET", json=None, retries=3):
    import httpx
    for attempt in range(retries):
        try:
            if method == "GET":
                r = httpx.get(url, timeout=2)
            else:
                r = httpx.post(url, json=json, timeout=2)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            log_event(f"Retry {attempt+1} failed for {url}: {e}")
            time.sleep(1)
    raise Exception(f"All retries failed for {url}")

def sanity_check(value):
    if not value or not isinstance(value, str):
        raise ValueError("Sanity check failed: value is not a valid string")
