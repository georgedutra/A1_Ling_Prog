import pandas as pd
import numpy as np

# Question 1: Wich album has the higher music duration average?
# Question 2: Is there any relation between the music's popularity and it being explicit or not?

def question_1(df:pd.DataFrame):
    """Receives a DataFrame with musics information, and print at the terminal wich album has the higher music duration mean.

    :param df: DataFrame with an index named 'Album' and a column named 'tracks_duration_ms' with the track's duration as numbers (in miliseconds)
    :type df: pd.DataFrame
    """
    try:
        # Takes a list with all album's names
        albums_list = np.unique(df.index.get_level_values("Album"))
        higher_duration = 0
        album_name = ""
        
        for album in albums_list:
            # For each album name, we make a cross-selection in the dataframe and calculates the duration mean
            album_durations = df.xs(album)["tracks_duration_ms"]
            duration_mean = album_durations.mean()
                        
            # For each mean, we register the current mean and it's album name if it's higher than all previous
            if duration_mean > higher_duration:
                higher_duration = duration_mean
                album_name = album
    except KeyError as error:
        print(error, "The dataframe must have an index called 'Album' and a column called 'tracks_duration_ms'.")
    else:
        print(f"\nThe album with the higher duration mean is {album_name}, with an average music duration of {higher_duration} miliseconds.\n\n", "="*60, sep="")

def question_2(df:pd.DataFrame):
    """Receives a DataFrame with musics information, and print at the terminal wheter the music's popularity is related to the lyrics being explicit or not

    :param df: DataFrame with a column named 'tracks_popularity' with numbers and other column named 'tracks_explicit' with booleans
    :type df: pd.DataFrame
    """
    try:
        correlation_df = df[["tracks_popularity", "tracks_explicit"]].corr()
    except KeyError as error:
        print(error, "The dataframe must have a column called 'tracks_popularity' and other column called 'tracks_explicit'.")
    else:
        if abs(correlation_df.iloc[0,1]) > 0.9:
            print(f"\nThe music's popularity is highly related to the music's lyrics being explicit or not.\n\n", "="*60, sep="")
        elif abs(correlation_df.iloc[0,1]) > 0.5:
            print(f"\nThe music's popularity is moderately related to the music's lyrics being explicit or not.\n\n", "="*60, sep="")
        else:
            print(f"\nThe music's popularity is not related to the music's lyrics being explicit or not.\n\n", "="*60, sep="")

#############################################################
# Teste com csv

df = pd.read_csv("TNBH_Data.csv", index_col=[0,1])

# question_1(df)
question_2(df)
