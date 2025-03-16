import requests
import json
from numpy import array_equal

testaddr = "https://olimp.miet.ru/ppo_it"

def getMap(addr=testaddr):
    r = requests.get(f"{addr}/api")
    data = json.loads(r.text)
    tile = data["message"]["data"]
    return tile


def getCoordsAndPrice(addr=testaddr) -> list:
    r = requests.get(f"{addr}/api/coords")
    data = json.loads(r.text)
    listener = data["message"]["listener"]
    sender = data["message"]["sender"]
    price = data["message"]["price"]
    return listener, sender, price

def getFullMap(addr=testaddr) -> list:
    alltiles = ['test']
    while len(alltiles) < 16:
        r = requests.get(f"{addr}/api")
        data = json.loads(r.text)
        tile = data["message"]["data"]
        for i in range(len(alltiles)):
            print(f"Checking {alltiles[i]} and {tile}")
            if not(array_equal(alltiles[i], tile)): alltiles.append(tile); 
    return alltiles[1::]
print(getFullMap())