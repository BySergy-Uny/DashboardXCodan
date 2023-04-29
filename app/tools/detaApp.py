from deta import Deta
from dotenv import dotenv_values
config = dotenv_values("./.env")

connector = Deta(config['DETA_PROJECT_KEY'])

users = connector.Base("users")
dataBase = connector.Base("data")
dataDrive = connector.Base("Drive") 
users.put({"username": "dXCodanAdmin", "token": 'cac95455060e8efb9b84b22a71d1e76769c990408555459e0f870cdb50a89fd9', "key": "000000"})

