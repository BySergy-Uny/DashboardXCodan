from pymongo import MongoClient

class databaseTool:

    def __init__(self, config) -> None:
        self.client = self.get_client(config)
        self.actual_db = ''
        self.actual_collection = ''
        self.pointer = None


    def get_client(self, config):
    
        url = config['MONGODB_CONNECTION_URL'] + "/"
        
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(url)
        
        # Create the database for our example (we will use the same database throughout the tutorial
        return client
    
    def get_databases_names(self):
        return self.client.list_database_names()
    
    def get_collections_names(self):
        return self.client[self.actual_db].list_collection_names()
    
    def insert_into_collection(self, item):
        try:
            self.pointer.insert_one(item)
            return True
        except:
            return False
    
    def search_into_collection(self, search):
        try:
            return self.pointer.find_one(search)
        except:
            return False     
    
    def set_database(self, database):
        if (database in self.get_databases_names()):
            self.pointer = self.client[database]
            self.actual_db = database
            return True
        else:
            return False
    
    def set_collection(self, collection):
        if (collection in self.get_collections_names()):
            self.pointer = self.pointer[collection]
            self.actual_collection = collection
            return True
        else:
            return False



# EJEMPLO DE USO DE LA HERRAMIENTA 

# print("[+] bases de datos",  db_mongo.get_databases_names())
# print('[+] set users database ', db_mongo.set_database('users'))
# print("[+] collections ", db_mongo.get_collections_names())
# print('[+] set operadores collection ', db_mongo.set_collection('operadores'))

# origin_user = {
#     'userId': 13245546,
#     'username': 'DxAdminUser',
#     'email': 'Pruebas@gmail.com',
#     'token': 45962734
# }
# respuesta = db_mongo.insert_into_collection(origin_user)
# print('[+] insertar un elemento: ', respuesta)

from dotenv import dotenv_values

config = dotenv_values("./.env")
db_mongo = databaseTool(config)