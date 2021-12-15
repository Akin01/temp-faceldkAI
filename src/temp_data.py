import requests
import os

url = os.getenv('URL')


def post_data(data: dict):
    res = requests.post(url, data)
    return res


def data_ready(temp_obj: float = None, temp_env: float = None) -> dict:
    data = {
        "temp": {
            "obj": temp_obj,
            "env": temp_env
        }
    }

    return data
