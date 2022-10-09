""" Module that creates the dataframe with the data from Spotify and the lyrics from Letras Mus Br."""

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from spotify_api import get_tracks_data
from mus_br_letras import get_nbhd_songs

def make_MultiIndex(songs_dict):
    """Creates a pandas MultiIndex object that will be used for further indexation of
    the pandas DataFrame to be analyzed.

    :param songs_dict: A dictionary of dictionaries, where the keys of the most external 
    dictionary are the albums and its values are dictionaries. In the internal dictionaries, 
    the keys of each one of them are the columns or indexes of the pandas DataFrame to be built.
    :type songs_dict: dict.
    :return: Pandas MultiIndex object
    :rtype: pandas.core.indexes.multi.MultiIndex
    """
    array=[]
    for key in songs_dict.keys():
        for elements in songs_dict[key]["tracks_names"]:
            array.append(list([key,elements]))
    df=pd.DataFrame(array,columns=["Album","Music"])
    multi_index=pd.MultiIndex.from_frame(df)
    return multi_index

def make_songs_df(songs_dict):
    #ConectionError
    """Creates the pandas DataFrame that will be used for all data analysis.

    :param dic: A dictionary of dictionaries, where the keys of the most external 
    dictionary are the albums and its values are dictionaries. In the internal dictionaries, 
    the keys of each one of them are the columns or indexes of the pandas DataFrame to be built.
    :type dic: dict
    :return: Pandas DataFrame object
    :rtype: pandas.core.frame.DataFrame
    """    
    #get an arbitrary key of the main dictionary.
    main_dic_key=list(songs_dict.keys())[0]

    #get all the keys of an arbitrary internal dictionary 
    #(the sets of keys of any internal dictionary are the same).
    sub_dic_keys=list(songs_dict[main_dic_key].keys())

    #Creates an empty DataFrame with the internal dictionary keys as columns, 
    #(except the "Music" key that will be part of the MultiIndex).
    df=pd.DataFrame(columns=sub_dic_keys).drop("tracks_names", axis=1)

    #Concatenates all individual DFs of each album into one DF with a MultiIndex.
    for key in songs_dict.keys():
        data=songs_dict[key]
        partial_df=pd.DataFrame(data).drop("tracks_names", axis=1)
        df=pd.concat([df,partial_df])
 
    df_spotify=df.set_index(make_MultiIndex(songs_dict))
    
    #If needed to use the DF directly.
    return df_spotify

def append_lyrics_to_df(songs_df):
    """Function that takes the dataframe created with spotify data and appends the lyrics scrapped from Letras Mus Br.

    :param songs_df: Dataframe generated with only the spotify data.
    :type songs_df: pandas.core.frame.DataFrame
    :return: Dataframe with lyrics appended.
    :rtype: pandas.core.frame.DataFrame
    """
    lyrics_dict = get_nbhd_songs()
    normal_lyrics_names = dict() #dictionary that takes the normalized name as key and its original as the value
    for lyrics_name in lyrics_dict:
      normal_lyrics_names[lyrics_name.replace(" ", "").upper()] = lyrics_name

    songs_df["Lyrics"] = "" #creates the empty dataframe column
    for element in songs_df.index.values:
      if element[1].replace(" ", "").upper() in normal_lyrics_names: #normalizes and compare the index with the values in the normalized lyrics names
        songs_df.loc[element].loc["Lyrics"] = lyrics_dict[normal_lyrics_names[element[1].replace(" ", "").upper()]] #If its in the normalized dictionary, appends its songs lyrics to the column "Lyrics".
    return songs_df

def save_csv(csv_name, songs_df):
    """Function that saves the dataframe into a .csv, so we don't have to rerun the scrapper all the time.

    :param csv_name: Name of the .csv that will be generated
    :type songs_df: str
    :param songs_df: Dataframe with the lyrics appended
    :type songs_df: pandas.core.frame.DataFrame
    """
    songs_df.to_csv(csv_name)
    
    
def create_final_dataframe(csv_name):
    """Function that aggregates the necessary functions and generates the .csv and returns the dataframe in case you need it.

    :param csv_name: Name of the .csv that will be generated. Must have the ".csv at the end.
    :type songs_df: str
    :return: Final dataframe with lyrics in it.
    :rtype: pandas.core.frame.DataFrame
    """
    songs_dict = get_tracks_data()
    songs_df = make_songs_df(songs_dict)
    songs_lyrics_df = append_lyrics_to_df(songs_df)
    save_csv(csv_name, songs_lyrics_df)
    return songs_lyrics_df