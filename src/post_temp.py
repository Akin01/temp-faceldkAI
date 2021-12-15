import requests
import os

url = os.getenv('URL')


def postTemp(data: dict):
    res = requests.post(url, data)
    return res
