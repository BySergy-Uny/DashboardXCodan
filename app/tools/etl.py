import pandas as pd
import numpy as np
from detaApp import *

db = dataBase


# Extraction 

def extraction(df={}):
    df = {}
    df['nodos'] = pd.read_csv('app/assets/reg_nodes_measures.csv')
    return df

# Transform

def transform(df):
    df_auxiliar = pd.DataFrame()
    df_auxiliar['timestamp'] = df['nodos']['time_index']
    df_auxiliar['temperatura'] = df['nodos']['temperatura']
    df_auxiliar['humedad'] = df['nodos']['humedad']
    df_auxiliar['tvoc'] = df['nodos']['tvoc']
    df_auxiliar['eco2'] = df['nodos']['eco2']
    df_auxiliar['nodo'] = df['nodos']['entity_id']

    df_auxiliar['timestamp'] = pd.to_datetime(df_auxiliar['timestamp'], unit='ms')
    df_auxiliar['timestamp'] = df_auxiliar['timestamp'].apply(lambda x: pd.Timestamp(x).timestamp())

    df['nodos'] = df_auxiliar.reset_index(drop=True)
    return df

# Upload

def upload(df):
    for dfi in df:
        print('[+] To upload data', dfi)
        name = dfi
        dfi = df[dfi]
        bins = np.linspace(dfi['timestamp'].max(),
                        dfi['timestamp'].min(),
                            int(len(dfi.index)/1000))
        i = np.digitize(dfi['timestamp'], bins)

        dfi['dataframe']=i

        with ChargingBar('[+] Uploading', max=len(bins), suffix='[%(remaining)d|%(percent)d%%]') as bar:
            for i in range(min(i), max(i)+1):
                df_aux = dfi[dfi['dataframe'] == i]
                del df_aux['dataframe']
                db.put(data={'timestamp':bins[i], 'type':name, 'data':df_aux.to_dict(orient='records')}) 
                bar.next()
        bar.finish()  

        print("[+] Total Upload", len(dfi))

        
from progress.bar import ChargingBar

def put_many(dframe):
    with ChargingBar('[+] Uploading', max=len(dframe), suffix='%(index)-%(max)|%(percent)d%%') as bar:
        for i in range(0,len(dframe),24):
            z = i+24
            if z>=len(dframe):
                z = len(dframe)-1
            bar.next(25)
            db.put_many(dframe[i:z]) 

def put_many_sec(dframe):
    with ChargingBar('[+] Uploading', max=len(dframe), suffix='%(index)-%(max)|%(percent)d%%') as bar:
        for i in range(0,len(dframe)):
            try:
                db.put(dframe[i])  
                bar.next()
            except:
                print(i, dframe[i])
                break



def delete_many_sec(items):
    with ChargingBar('[+] Deleting', max=len(items), suffix='%(remaining)d | %(percent)d%%') as bar:
        for i in items:
            try:
                db.delete(key=i['key']) 
                bar.next()
            except:
                break
        bar.finish()

def delete_all():
    all_items = []
    try:
        print('[+] Feching ...')
        res = db.fetch(limit=1000)
        all_items = res.items 
    except:
        print("[!] Error Fetch")

    while res.last:
            
        try:
            res = db.fetch(limit=1000, last=res.last)
            all_items += res.items
            
        except:
            print("[!] Error Fetch")
            break
    print("[+] Total Fetched", len(all_items))
    delete_many_sec(all_items)




#  ETL Process

delete_all()
df = extraction()
df = transform(df)
upload(df)



