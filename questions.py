import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from create_df import make_df,make_MultiIndex

dic={"album1":{"Music":["music11", "music12","music13"], "duration":[0.55,0.65,0.54], 
                "views":[1250,1200,1300], "popularity":[100,50,60]},
     "album2":{"Music":["music21", "music22","music23"], "duration":[0.75,0.85,0.75], 
                "views":[1150,1100,1050], "popularity":[80,30,60]}}


sns.set_theme(context="paper", style="darkgrid")

def song_popularity_album(dic):
    """Create a bar chart of each album to answer the question "which songs are most 
    listened and least listened per album?".

    :param dic: Dictionary
    :type dic: dict
    """    
    df=make_df(dic)
    
    #A numpy array with the values of the first level of MultiIndex.
    albums=np.unique(make_MultiIndex(dic).get_level_values("Album"))

    for album in albums:
        #Select the row of the DataFrame related to one specific album.
        df_sliced=df.xs(album)
        
        #The index of the most popular song (wich is the name of the song and the 
        #second level of MultiIndex).
        most_popular=df_sliced["popularity"].astype(float).idxmax()
        
        #The index of the least popular song (wich is the name of the song and the 
        #second level of MultiIndex).
        least_popular=df_sliced["popularity"].astype(float).idxmin()

        #Seaborn to make the visualization.
        plot=sns.barplot(data=df_sliced, x=df_sliced.index, y="popularity")

        #Y-axis label
        plot.set(ylabel="Popularity")

        #Title.
        plt.title(label=f"{album}", loc="center", pad=10)

        #Footnote.
        plt.figtext(0.1, 0.01, f"""The most popular song of {album} is 
{most_popular} and the least is {least_popular}.""", ha="left", fontsize=8, 
bbox={"facecolor": "white", "pad": -10})

        #Save and close the plot.
        plt.savefig(f"imgs/{album}_popularity.png")
        plt.close()

def song_duration_album(dic):
    """Create a bar chart of each album to answer the question "which songs are longest 
    and which are shortest per album?".

    :param dic: Dictionary
    :type dic: dict
    """    
    df=make_df(dic)
    
    #A numpy array with the values of the first level of MultiIndex.
    albums=np.unique(make_MultiIndex(dic).get_level_values("Album"))

    for album in albums:
        #Select the row of the DataFrame related to one specific album.
        df_sliced=df.xs(album)
        
        #The index of the longest song (wich is the name of the song and the 
        #second level of MultiIndex).
        longest=df_sliced["duration"].astype(float).idxmax()
        
        #The index of the shortest song (wich is the name of the song and the 
        #second level of MultiIndex).
        shortest=df_sliced["duration"].astype(float).idxmin()

        #Seaborn to make the visualization.
        plot=sns.barplot(data=df_sliced, x=df_sliced.index, y="duration")

        #Y-axis label
        plot.set(ylabel="Duration")

        #Title.
        plt.title(label=f"{album}", loc="center", pad=10)

        #Footnote.
        plt.figtext(0.1, 0.01, f"""The longest song of {album} is 
{longest} and the shortest is {shortest}.""", ha="left", fontsize=8, 
bbox={"facecolor": "white", "pad": -10})

        #Save and close the plot.
        plt.savefig(f"imgs/{album}_duration.png")
        plt.close()