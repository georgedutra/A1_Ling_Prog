import numpy as np
import pandas as pd

import wordcloud as wc
import matplotlib.pyplot as plt
import multidict as mdic

def lyrics_concat(df):
    """Recebe um DataFrame de músicas e retorna uma string com todas as lyrics concatenadas

    :param df: DataFrame de músicas com uma coluna 'Lyric' que possui as letras de cada música como string
    :type df: pandas.DataFrame
    :return: string com todas as letras de músicas do artista ou banda concatenadas
    :rtype: str
    """
    lista_lyrics = list(df["Lyric"])
    string_concatenada = " ".join(lista_lyrics)
    return string_concatenada

def lyrics_albuns(df):
    """Recebe um dataframe de músicas e retorna um dicionário com os nomes dos albuns como chaves e uma string como valor com as letras de todas as músicas do álbum concatenadas. 

    :param df: Dataframe com um Multi-Index 'Album' (nome do álbum o qual a música pertence), e uma coluna 'Lyric' com as letras de cada música como strings
    :type df: pandas.DataFrame
    :return: Dicionário com keys sendo os nomes de cada álbum da banda, e values sendo uma string de todas as letras das músicas do álbum concatenadas
    :rtype: dict
    """

    dict_lyrics = {} # Dicionário que será retornado no final
    albuns = np.unique(df.index.get_level_values("Album")) # Cria um array com o nome de todos os álbuns
    for nome_album in albuns:
        dict_lyrics[nome_album] = lyrics_concat(df.xs(nome_album))
    return dict_lyrics

def nomes_musicas(df):
    """Recebe um dataframe de músicas e retorna uma string com todos os nomes das músicas concatenadas

    :param df: Dataframe com um Multi-Index 'Nome' (nome da música)
    :type df: pandas.DataFrame
    :return: string com todos os nomes das músicas concatenados
    :rtype: str
    """
    lista_musicas = list(df.index.get_level_values("Nome"))
    nomes_musicas = " ".join(lista_musicas)
    return nomes_musicas



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

print(nomes_musicas(df))