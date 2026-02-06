from threading import Lock

_lock = Lock()

state = {
    "visits": 0,
    "sales": 0,
    "temperature": None,
    "humidity": None
}

def register_visit():
    with _lock:
        state["visits"] += 1

def register_sales():
    with _lock:
        state["sales"] += 1

def update_environment(temp, hum):
    with _lock:
        state["temperature"] = temp
        state["humidity"] = hum

def get_state():
    with _lock:
        return state.copy()
