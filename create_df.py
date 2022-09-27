import pandas as pd
import numpy as np

dic={"album1":{"musics":["music11", "music21"], "duration":[0.55,0.65], 
                "views":[1250,1200]},
     "album2":{"musics":["music12", "music22"], "duration":[0.75,0.85], 
                "views":[1150,1100]}}

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
        for elements in dic[key]["musics"]:
            array.append(list([key,elements]))
    df=pd.DataFrame(array,columns=["albums","musics"])
    multi_index=pd.MultiIndex.from_frame(df)
    return multi_index

def make_df(dic):
    """Creates the pandas DataFrame that will be used for all data analysis.

    :param dic: A dictionary of dictionaries, where the keys of the most external 
    dictionary are the albums and its values are dictionaries. In the internal dictionaries, 
    the keys of each one of them are the columns or indexes of the pandas DataFrame to be built.
    :type dic: dict
    :return: Pandas DataFrame object
    :rtype: pandas.core.frame.DataFrame
    """    
    main_dic_key=list(dic.keys())[0]
    sub_dic_keys=list(dic[main_dic_key].keys())
    df=pd.DataFrame(columns=sub_dic_keys).drop("musics", axis=1)
    for key in dic.keys():
        data=dic[key]
        partial_df=pd.DataFrame(data).drop("musics", axis=1)
        df=pd.concat([df,partial_df])
    df_final=df.set_index(make_MultiIndex(dic))
    return df_final




