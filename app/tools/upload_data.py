from detaApp import *

dataDrive.put("reg_nodes_measures.csv", path='app/assets/reg_nodes_measures.csv')
dataDrive.put("generador_temp.csv", path='app/assets/generador_temp.csv')

# large_file = drive.get('reg_nodes_measures.csv')
# with open("app/assets/reg_nodes_measures.csv", "wb+") as f:
#   for chunk in large_file.iter_chunks(4096):
#       f.write(chunk)
#   large_file.close()
