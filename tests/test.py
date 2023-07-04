# from app.tools.detaApp import *
from datetime import datetime
import pandas as pd

# dataBaseTest = connector.Base("data-test")
print('Carga generador')
df = pd.read_csv('./app/assets/generador_temp.csv')
print(df.head())

print(df.loc[0]['pred'])

