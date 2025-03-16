import requests
import json

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
    alltiles = []
    hashable = set()
    while len(alltiles) < 16:
        r = requests.get(f"{addr}/api")
        data = json.loads(r.text)
        tile = data["message"]["data"]
        tileString = ""
        for i in tile:
            tileString += "".join(str(i))
        if tileString not in hashable: hashable.add(tileString); alltiles.append(tile)
    return alltiles