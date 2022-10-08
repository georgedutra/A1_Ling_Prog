"""Module to generate TagCloud images based on music databases"""

import numpy as np
import pandas as pd
import wordcloud as wc
import multidict
import re

def lyrics_all(df):
    """Receives a DataFrame with musics and returns a string with every lyric concatenated

    :param df: musics DataFrame with one column 'Lyrics' that has each music's lyrics as strings
    :type df: pd.DataFrame
    :return: string with every artist's music lyrics concatenated
    :rtype: str
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The function only accepts DataFrames as parameters.")
    
    try:
        lyrics_list = list(df["Lyrics"].astype("str"))
        concatenated_string = " ".join(lyrics_list)
    
    except KeyError:
        print("DataFrame has no column 'Lyrics'.")
        return ""
    except TypeError:
        print("Some of the lyrics are not strings, and can't be converted.")
        return ""
    
    else:
        return concatenated_string

def lyrics_albuns(df):
    """Receives a dataframe with musics and return a dictionary with all albums names and all music's lyrics in each album concatenated as a string.

    :param df: Dataframe with an 'Album' Multi-Index (the name of the album each music belongs to), and a 'Lyrics' column with each song's lyrics as strings
    :type df: pd.DataFrame
    :return: Dictionary with albums names as keys, and all music's lyrics in each album concatenated as a string, as the key's values.
    :rtype: dict
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The function only accepts DataFrames as parameters.")
    
    try:
        dict_lyrics = {} # Dictionary to be returned in the end
        albums = np.unique(df.index.get_level_values("Album")) # Creates an array with every album's names
        for album_name in albums:
            dict_lyrics[album_name] = lyrics_all(df.xs(album_name))
    
    except KeyError:
        print("DataFrame has no index 'Album'.")
        return {}
    except TypeError:
        print("Some of the album's titles are not strings.")
        return {}
        
    else:
        return dict_lyrics

def music_names(df):
    """Receives a dataframe with musics and returns a concatenated string with every song's names

    :param df: Dataframe with a Multi-Index called 'Music' (music's name)
    :type df: pd.DataFrame
    :return: string with all musics names concatenated
    :rtype: str
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The function only accepts DataFrames as parameters.")
    try:
        music_list = list(df.index.get_level_values("Music"))
        concat_names = " ".join(music_list)

    except KeyError:
        print("DataFrame has no index 'Music'.")
        return ""
    except TypeError:
        print("Some of the music names are not strings.")
        return ""

    else:    
        return concat_names

def frequency(text):
    """Receives a string, and returns a multidict with each word's number of ocurrencies in the string 

    :param text: A string with the text wished to count each word's frequency
    :type text: str
    :return: A Multidict with words as keys and the word's frequencies as values
    :rtype: multidict.MultiDict
    """
    if not isinstance(text, str):
        raise TypeError("The function only accepts strings as parameter")

    # This creates both a MultiDict and a dictionary, because for some reason the WordCloud library asks for it
    frequency_multidict = multidict.MultiDict()
    freq_dict = {}

    # Then, we split the text word by word, and count each ocurrence
    for word in text.split(" "):
        # This regex line excludes common prepositions and articles we don't want to count
        if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be|&|-|nan", word):
            continue
        appears = freq_dict.get(word, 0)
        freq_dict[word.lower()] = appears + 1

    # Let's remove some unwished characters
    if "" in freq_dict:
        freq_dict.pop("")
    
    # Finally, we transfer all the information from the standard dict to the MultiDict, and return it
    for key in freq_dict:
        frequency_multidict.add(key, freq_dict[key])
    return frequency_multidict

def frequency_generator(frequencies, file_name):
    """Receives a frequency MultiDict, and creates a tagcloud named '{file_name}.png'

    :param frequencies: MultiDict with words as keys and frequencies as values
    :type frequencies: multidict.MultiDict
    :param file_name: string that defines the name of the image file to be saved
    :type file_name: str
    """
    if len(frequencies) < 10:
        print(f"The amount of words is insufficient to create the archive {file_name}.png")
        return
    cloud = wc.WordCloud(max_words=10000, max_font_size=40, relative_scaling=0).generate_from_frequencies(frequencies)
    cloud.to_file(f"images/{file_name}.png") 

def generate_cloud_lyrics(df):
    """Receives a DataFrame with musics and generates a TagCloud image named 'all_lyrics_tagcloud.png' according to the most frequent words in all lyrics

    :param df: A DataFrame with a 'Lyrics' column, with all music's lyrics as strings
    :type df: pd.DataFrame
    """
    frq_dict = frequency(lyrics_all(df))
    frequency_generator(frq_dict, "all_lyrics_tagcloud")

def generate_cloud_albuns(df):
    """Receives a DataFrame with musics and generates a TagCloud image named '{album_name}_tagcloud.png' according to the most frequent words in each album's lyrics

    :param df: A DataFrame with an index called 'Album' and a 'Lyrics' column, with all music's lyrics as strings
    :type df: pd.DataFrame
    """
    # Picks a dictionary with each album's lyrics, and generate a tagcloud for each album
    albuns = lyrics_albuns(df)
    for key in albuns:
        frq_dict = frequency(albuns[key])
        frequency_generator(frq_dict, f"{key}_tagcloud") 

def generate_cloud_music_names(df):
    """Receives a DataFrame with musics and generates a TagCloud image named 'names_tagcloud.png' according to the most frequent words in all music's titles

    :param df: A DataFrame with an index called 'Name', with all music's names as strings
    :type df: pd.DataFrame
    """
    frq_dict = frequency(music_names(df))
    frequency_generator(frq_dict, "names_tagcloud")
