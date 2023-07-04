import pandas as pd
from ..tools.detaApp import *
from datetime import datetime
import random


class NodeMeasureTest():
     
    def __init__(self):
        self.db = connector.Base('data-test')
        self.delete_all()
        self.df_generator_temp = pd.read_csv('./app/assets/generador_temp.csv')
        self.max_index = len(self.df_generator_temp)-1
        self.index_generator = 20

    def delete_all(self):
        print('[+] Delete all')
        
        res = self.db.fetch()
        all_items = res.items
        
        # fetch until last is 'None'
        while len(all_items)>1 or res.last :
            print('[+] Delete all',len(all_items))
            while len(all_items)>0:
                item = all_items.pop(0)
                self.db.delete(item['key'])
            res = self.db.fetch(last=res.last)
            all_items += res.items
        
    def query_all(self,query):
        res = self.db.fetch(query=query)
        all_items = res.items

        # fetch until last is 'None'
        while res.last:
            res = self.db.fetch(query=query,last=res.last)
            all_items += res.items

        df = pd.DataFrame(all_items)

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

        df = df.sort_values(by=['timestamp'], ascending=False)

        return df 

    def get_update(self):

        data = {
            "index_generator": self.index_generator,
            "eco2": 0,
            "humedad": 0,
            "nodo": "nodo1",
            "temperatura": 0,
            "timestamp": 0,
            "tvoc": 1
        }

        now = datetime.now()
        now = int(now.timestamp())

        data['timestamp'] = now
        
        row_generator = self.df_generator_temp.loc[self.index_generator]
        generator_temp = [row_generator['pred'],row_generator['lower_bound'], row_generator['upper_bound']]
        
        data_temp = random.choice(generator_temp)

        escala_temp = (data_temp-10) / (46-10)

        data_eco2 = escala_temp * (32768 - 1) + 1 
        data_humedad = escala_temp * (32)
        data_tvoc = escala_temp * (29206)

        data['eco2'] = data_eco2
        data['humedad'] = data_humedad
        data['temperatura'] = data_temp
        data['tvoc'] = data_tvoc

        test = connector.Base('data-test')
        test.put(data)

        self.index_generator += 60
        self.index_generator = self.index_generator % self.max_index


    def get_frame(self):
        return self.query_all(None)





