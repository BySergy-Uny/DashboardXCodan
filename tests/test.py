
from datetime import datetime
import pandas as pd

import sys
# Insert the path of modules folder 
sys.path.insert(0, "./app/tools")

from detaApp import dataDrive
response = dataDrive.get("reg_nodes_measures.csv")

df = pd.read_csv(response)


print(df.head())
