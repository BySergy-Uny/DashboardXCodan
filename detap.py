

from deta import Deta
from dotenv import dotenv_values

config = dotenv_values("./.env")

db = Deta(config['DETA_PROJECT_KEY'])

users = db.Base("users")

users.put({"username": "pepe", "token": 'b60e4d6c465515f6a638c1ee89810e4d2e9d3114a2b26cb709c37e45cf9641e5', "key": "pepe"})

f = users.fetch({"username": 'pepe'})

print(f.items[0]['token'])