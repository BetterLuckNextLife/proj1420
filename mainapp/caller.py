import requests
import json

testaddr = "https://olimp.miet.ru/ppo_it"

def getTestMap():
    r = requests.get(testaddr + "/api")
    data = json.loads(r.text)
    tile = data["message"]["data"]
    return tile


def getTestCoordsAndPrice() -> list:
    r = requests.get(testaddr + "/coords")
    data = json.loads(r.text)
    listener = data["message"]["listener"]
    sender = data["message"]["sender"]
    price = data["message"]["price"]
    return listener, sender, price

print(getTestCoordsAndPrice())
print(getTestMap())