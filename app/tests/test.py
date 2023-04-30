import pandas as pd
from deta import Deta
from dotenv import dotenv_values
from datetime import datetime
import random
config = dotenv_values("./.env")


def delete_all(db):
    print('[+] Delete all')
    
    res = db.fetch()
    all_items = res.items
    
    # fetch until last is 'None'
    while len(all_items)>1 or res.last :
        print('[+] Delete all',len(all_items))
        while len(all_items)>0:
            item = all_items.pop(0)
            db.delete(item['key'])
        res = db.fetch(last=res.last)
        all_items += res.items
        
def query_all(db, query):
    res = db.fetch(query=query)
    all_items = res.items

    # fetch until last is 'None'
    while res.last:
        res = db.fetch(query=query,last=res.last)
        all_items += res.items

    df = pd.DataFrame(all_items)

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

    df = df.sort_values(by=['timestamp'], ascending=False)

    return df 

def get_update():

    data = {
        "eco2": 401,
        "humedad": 11,
        "nodo": "nodo1",
        "temperatura": 50,
        "timestamp": 1630724538,
        "tvoc": 1
    }

    now = datetime.now()
    now = int(now.timestamp())

    data['timestamp'] = now
    data['eco2'] = random.randint(200,400)
    data['humedad'] = random.randint(5,20)
    data['temperatura'] = random.randint(30,100)
    data['tvoc'] = random.randint(0,10)

    test = connector.Base('data-test')
    test.put(data)


def get_frame():
	test = connector.Base('data-test')
	return query_all(test,None)

connector = Deta(config['DETA_PROJECT_KEY'])

db = connector.Base('data-test')
delete_all(db)
get_update()


