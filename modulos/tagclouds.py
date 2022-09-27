import numpy as np
import pandas as pd
from PIL import Image
import wordcloud as wc
import multidict

def lyrics_concat(df):
    """Receives a DataFrame with musics and returns a string with every lyric concatenated

    :param df: musics DataFrame with one column 'Lyric' that has each music's lyrics as strings
    :type df: pandas.DataFrame
    :return: string with every artist's music lyrics concatenated
    :rtype: str
    """
    lyrics_list = list(df["Lyric"])
    concatenated_string = " ".join(lyrics_list)
    return concatenated_string

def lyrics_albuns(df):
    """Receives a dataframe with musics and return a dictionary with all albums names and all music's lyrics in each album concatenated as a string.

    :param df: Dataframe with an 'Album' Multi-Index (the name of the album each music belongs to), and a 'Lyric' column with each song's lyrics as strings
    :type df: pandas.DataFrame
    :return: Dictionary with albums names as keys, and all music's lyrics in each album concatenated as a string, as the key's values.
    :rtype: dict
    """

    dict_lyrics = {} # Dictionary to be returned in the end
    albums = np.unique(df.index.get_level_values("Album")) # Creates an array with every album's names
    for album_name in albums:
        dict_lyrics[album_name] = lyrics_concat(df.xs(album_name))
    return dict_lyrics

def music_names(df):
    """Receives a dataframe with musics and returns a concatenated string with every song's names

    :param df: Dataframe with a Multi-Index called 'Music' (musics name)
    :type df: pandas.DataFrame
    :return: string with all musics names concatenated
    :rtype: str
    """
    music_list = list(df.index.get_level_values("Music"))
    concat_names = " ".join(music_list)
    return concat_names

####################################################################################################################
# creating a fiction dataframe while I dont have the oficial one
album = ["Album 1","Album 1","Album 2","Album 2"]
names = ["Daddy Issues", "ABC", "DEF", "GHI"]
indexes = pd.MultiIndex.from_arrays([album, names], names=("Album", "Music"))
columns = ["Released", "Popularity", "Lyric"]

dados = [[1982, 2600000, "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent molestie rhoncus risus. Phasellus augue quam"], 
[2000,100000,"euismod vel neque eget, egestas finibus felis. Fusce facilisis odio tellus, eget sollicitudin lacus venenatis ut. Nulla laoreet magna tristique ante pharetra tincidunt."],
[2007,600000,"usce facilisis odio tellus, eget sollicitudin lacus venenatis ut. Nulla laoreet magna tristique ante pha"],
[2016,3000000,"Integer in enim nibh. Curabitur consectetur purus commodo, pellentesque nulla ac, rhoncus turpis. Maecenas at dui eget tortor porta ornare."]]

df = pd.DataFrame(dados, index=indexes, columns=columns)
