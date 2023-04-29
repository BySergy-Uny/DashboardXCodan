from detaApp import *
import pandas as pd
from datetime import datetime


qry  = {"type":"temp"}
qry  = {"timestamp?gt":1630724501, "timestamp?lt":1630905742}
qry = {"timestamp?r": [1609459200.0, 1627515900.0]}

def query_all(query):
    res = dataBase.fetch(query=query)
    all_items = res.items

    # fetch until last is 'None'
    while res.last:
        res = dataBase.fetch(query=query,last=res.last)
        all_items += res.items

    data = []
    for i in all_items:
        data += i['data']

    df = pd.DataFrame(data)

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

    return df 

print(query_all(qry))

# print(datetime.now())
# date = datetime.now()
# date = pd.Timestamp(date).timestamp()
# print(date)