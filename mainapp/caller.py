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
    alltiles = []
    while len(alltiles) < 16:
        r = requests.get(f"{addr}/api")
        data = json.loads(r.text)
        tile = data["message"]["data"]
        if tile not in alltiles: alltiles.append(tile)

    print(type(json.dumps(alltiles)))
    return alltiles

def get16UniqueTiles():
    unique_tiles = set()
    while len(unique_tiles) < 16:
        tile = getTestMap()
        tile_tuple = tuple(tuple(row) for row in tile)
        unique_tiles.add(tile_tuple)
    return list(unique_tiles)

getFullMap()