import requests
import json

def getTestData() -> list:
    r = requests.get("https://olimp.miet.ru/ppo_it/api")
    data = json.loads(r.text)
    print(data["message"]["data"])