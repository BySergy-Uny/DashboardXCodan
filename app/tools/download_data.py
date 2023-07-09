from detaApp import *

def download(name, path):
    large_file = dataDrive.get(name)
    with open(path, "wb+") as f:
        for chunk in large_file.iter_chunks(4096):
            f.write(chunk)
    large_file.close()

download("reg_nodes_measures.csv", path='app/assets/reg_nodes_measures.csv')
download("reg_nodes_temp.xlsx", path='app/assets/reg_nodes_temp.xlsx')