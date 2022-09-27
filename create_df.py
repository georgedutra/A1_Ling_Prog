import pandas as pd
import numpy as np

dic={"album1":{"musicas":["musica11", "musica21"], "duração":[0.55,0.65]}, "album2":{"musicas":["musica12", "musica22"], "duração":[0.55,0.65]}}

def make_MultiIndex(dic):
    """Essa função cria um objeto MultiIndex para ser usado nos dataframes que serão analisados.

    :param dic: Dicionário com os dados obtidos no web-scrapping
    :type dic: dict
    :return: Objeto MultiIndex do pandas
    :rtype: pandas.core.indexes.multi.MultiIndex
    """
    lista=[]
    for key in dic.keys():
        for e in dic[key]["musicas"]:
            lista.append(list([key,e]))
    df=pd.DataFrame(lista,columns=["albuns","musicas"])
    multi_index=pd.MultiIndex.from_frame(df)
    return multi_index

