from tkinter import N
import wordcloud as wc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import multidict as mdic

def lyrics_albuns(df):
    """Recebe um dataframe de músicas com Multi-Index de nível 1 = Album e nível 2 = Nome, e retorna um dicionário com os albuns como chaves e uma string como valor com as letras de todas as músicas do álbum concatenadas. 

    Args:
        df (pd.DataFrame): DataFrame com Multi-Index de dois níveis, sendo o primeiro o nome dos álbuns, e o segundo, o nome das músicas
    """
    # Criando um set e armazenando nele os nomes de todos os álbuns que aparecem no df
    set_albuns = set()
    for indice in df.index:
        set_albuns.add(indice[0])
    # Acessando o dataframe álbum por álbum através dos nomes armazenados no set
    for album in set_albuns:
        print(df.xs(f"{album}"))



####################################################################################################################
# criando um dataframe de exemplo enquanto nao tem o oficial
album = ["Album 1","Album 1","Album 2","Album 2"]
nomes = ["Daddy Issues", "ABC", "DEF", "GHI"]
indices = pd.MultiIndex.from_arrays([album, nomes], names=("Album", "Nome"))
colunas = ["Lançamento", "Popularidade", "Lyric"]

dados = [[1982, 2600000, "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent molestie rhoncus risus. Phasellus augue quam"], 
[2000,100000,"euismod vel neque eget, egestas finibus felis. Fusce facilisis odio tellus, eget sollicitudin lacus venenatis ut. Nulla laoreet magna tristique ante pharetra tincidunt."],
[2007,600000,"usce facilisis odio tellus, eget sollicitudin lacus venenatis ut. Nulla laoreet magna tristique ante pha"],
[2016,3000000,"Integer in enim nibh. Curabitur consectetur purus commodo, pellentesque nulla ac, rhoncus turpis. Maecenas at dui eget tortor porta ornare."]]

df = pd.DataFrame(dados, index=indices, columns=colunas)
