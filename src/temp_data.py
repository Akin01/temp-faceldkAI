def data_ready(temp_obj: float = None, temp_env: float = None) -> dict:
    data = {
        "temp": {
            "obj": temp_obj,
            "env": temp_env
        }
    }

    return data
