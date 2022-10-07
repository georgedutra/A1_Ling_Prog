"""Module to answer the questions 1 to 6 from the group 2
"""

import numpy as np
import pandas as pd
import tagclouds as tag
import multidict

def dict_to_series(dict: dict | multidict.MultiDict) -> pd.Series:
    """Receives a dictionary with words and frequency numbers and returns a Series object sorted by descending values

    :param dict: Dictionary with words as keys and numbers as values
    :type dict: dict | multidict.MultiDict
    :return: Pandas Series with words as keys and numbers as values, sorted by descending values
    :rtype: pd.Series
    """
    indexes = dict.keys()
    values = dict.values()
    series = pd.Series(values, indexes)
    return series.sort_values(ascending=False)

def question_1(df: pd.DataFrame):
    """Receives a DataFrame with musics information and print at the console wich words are the most common among the band's album's titles 

    :param df: DataFrame with one MultiIndex named 'Album' with the band's album's names as strings
    :type df: pd.DataFrame
    """
    try:
        albums = np.unique(df.index.get_level_values("Album"))
        albums_string = " ".join(albums)
        albums_series = dict_to_series(tag.frequency(albums_string))
    except KeyError as error:
        print(f"{error}, DataFrame must have an index named 'Album' for question 1.")
    else:
        print("\nThe most common words in the band's album's titles are:\n", albums_series[0:5].index.values, "\n\n", "="*60, sep="")

def question_2(df: pd.DataFrame):
    """Receives a DataFrame with musics information and print at the console wich words are the most common among the band's music's titles 

    :param df: DataFrame with one MultiIndex named 'Music' with the band's music's names as strings
    :type df: pd.DataFrame
    """
    try:
        titles_series = dict_to_series(tag.frequency(tag.music_names(df)))
    except KeyError as error:
        print(f"{error}, DataFrame must have an index named 'Music' for question 2.")
    else:
        print("\nThe most common words in the band's music's titles are:\n", titles_series[0:5].index.values, "\n\nGenerated TagCloud with most common words in music's titles\n\n","="*60, sep="")
        tag.generate_cloud_music_names(df)

def question_3(df: pd.DataFrame):
    """Receives a DataFrame with musics information and print at the console wich words are the most common among each album's music's lyrics 

    :param df: DataFrame with one MultiIndex named 'Album' and one column named 'Lyric' with the band's music's lyrics as strings
    :type df: pd.DataFrame
    """
    try:
        lyrics = tag.lyrics_albuns(df)
        for album in lyrics:
            words_freq = dict_to_series(tag.frequency(lyrics[album]))
            print(f"\nThe most common words in the lyrics from the album {album} are:\n", words_freq[0:5].index.values,"\n\n","="*60, sep="")
        tag.generate_cloud_albuns(df)
        print("\nGenerated TagCloud with each album's lyric's most common words.", "\n\n","="*60, sep="")
    except KeyError as error:
        print(f"{error}, DataFrame must have an index named 'Album' and a column named 'Lyric' for question .")
        
def question_4(df: pd.DataFrame):
    """Receives a DataFrame with musics information and print at the console wich words are the most common among all music's lyrics 

    :param df: DataFrame with one column named 'Lyric' with the band's music's lyrics as strings
    :type df: pd.DataFrame
    """
    try:
        lyrics_freq = dict_to_series(tag.frequency(tag.lyrics_all(df)))
    except KeyError as error:
        print(f"{error}, DataFrame must have a column named 'Lyric' for question 4.")
    else:
        print("\nThe most common words in the lyrics from the whole band's discography are:\n", lyrics_freq[0:5].index.values, "\n\nGenerating TagCloud with all lyrics most common words...\n\n","="*60, sep="")
        tag.generate_cloud_lyrics(df)

def question_5(df: pd.DataFrame):
    """Receives a DataFrame with musics information and verify if at least half the albums have it's titles in some of it's music's lyrics  

    :param df: DataFrame with one MultiIndex named 'Album' and one column named 'Lyric' with the band's music's lyrics as strings
    :type df: pd.DataFrame
    """
    try:
        lyrics = tag.lyrics_albuns(df)
        ocurrencies = 0
    
        for album in lyrics:
            if album in lyrics[album]:
                ocurrencies += 1
    except KeyError as error:
        print(f"{error}, DataFrame must have an index named 'Album' and one column named 'Lyric' for question 5.")
    else:
        if ocurrencies >= (len(lyrics)/2):
            print("\nThis band's musics usually have the album's titles into it's lyrics!\n\n", "="*60,sep="")
        else:
            print("\nThis band's musics usually don't have the album's titles into it's lyrics.\n\n", "="*60,sep="")

def question_6(df: pd.DataFrame):
    """Receives a DataFrame with musics information and verify if at least half the musics have it's titles in it's own lyrics  

    :param df: DataFrame with one MultiIndex named 'Music' and one column named 'Lyric' with the band's music's lyrics as strings
    :type df: pd.DataFrame
    """
    try:
        music_list = list(df.index.get_level_values("Music"))
        ocurrencies = 0

        for music in music_list:
            music_df = df.xs(music, level="Music")
            if music in music_df.iloc[0]["Lyric"]:
                ocurrencies += 1
    except KeyError as error:
        print(f"{error}, DataFrame must have an index named 'Music' and one column named 'Lyric' for question 6.")
    else:
        if ocurrencies >= (len(music_list)/2):
            print("\nThis band's musics usually have the music's title into it's lyrics!\n\n", "="*60,sep="")
        else:
            print("\nThis band's musics usually don't have the music's titles into it's lyrics.\n\n", "="*60,sep="")
