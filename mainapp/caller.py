import requests
import json

testaddr = "https://olimp.miet.ru/ppo_it"

def getTestMap(addr=testaddr):
    r = requests.get(f"{addr}/api")
    data = json.loads(r.text)
    tile = data["message"]["data"]
    return tile


def getTestCoordsAndPrice(addr=testaddr) -> list:
    r = requests.get(f"{addr}/api/coords")
    data = json.loads(r.text)
    listener = data["message"]["listener"]
    sender = data["message"]["sender"]
    price = data["message"]["price"]
    return listener, sender, price