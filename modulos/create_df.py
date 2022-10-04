import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from spotify_api import get_tracks_data



def make_MultiIndex(dic):
    """Creates a pandas MultiIndex object that will be used for further indexation of
    the pandas DataFrame to be analyzed.

    :param dic: A dictionary of dictionaries, where the keys of the most external 
    dictionary are the albums and its values are dictionaries. In the internal dictionaries, 
    the keys of each one of them are the columns or indexes of the pandas DataFrame to be built.
    :type dic: dict.
    :return: Pandas MultiIndex object
    :rtype: pandas.core.indexes.multi.MultiIndex
    """
    array=[]
    for key in dic.keys():
        for elements in dic[key]["tracks_names"]:
            array.append(list([key,elements]))
    df=pd.DataFrame(array,columns=["Album","Music"])
    multi_index=pd.MultiIndex.from_frame(df)
    return multi_index

def make_df(dic):
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
    main_dic_key=list(dic.keys())[0]

    #get all the keys of an arbitrary internal dictionary 
    #(the sets of keys of any internal dictionary are the same).
    sub_dic_keys=list(dic[main_dic_key].keys())

    #Creates an empty DataFrame with the internal dictionary keys as columns, 
    #(except the "Music" key that will be part of the MultiIndex).
    df=pd.DataFrame(columns=sub_dic_keys).drop("tracks_names", axis=1)

    #Concatenates all individual DFs of each album into one DF with a MultiIndex.
    for key in dic.keys():
        data=dic[key]
        partial_df=pd.DataFrame(data).drop("tracks_names", axis=1)
        df=pd.concat([df,partial_df])
 
    df_spotify=df.set_index(make_MultiIndex(dic))
    #Save
    df_spotify.to_csv("final_df.csv")
    #If needed to use the DF directly.
    return df_spotify

make_df(get_tracks_data())
