import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('URL')


def post_data(data: dict):
    res = requests.post(url, data)
    return res


def data_ready(temp_obj: float = None, temp_env: float = None) -> dict:
    data = {
        "temp_obj": temp_obj,
        "temp_env": temp_env
    }
    return data
