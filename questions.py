import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from create_df import make_df,make_MultiIndex


dic={"album1":{"Music":["music11", "music12","music13"], "duration":[0.55,0.65,0.84], 
                "views":[1250,1200,1300], "popularity":[100,50,60]},
     "album2":{"Music":["music21", "music22","music23"], "duration":[0.75,0.85,0.95], 
                "views":[1150,1100,1050], "popularity":[80,30,40]}}


sns.set_theme(context="paper", style="darkgrid")

def set_highlight_palette(series, max_color = 'turquoise', min_color = "red", 
other_color = 'lightgrey'):
    max_val = series.max()
    min_val= series.min()
    pal = []
    for item in series:
        if item == max_val:
                pal.append(max_color)
        elif item == min_val:
                pal.append(min_color)
        else:
            pal.append(other_color)
    return pal

def read_csv():
    df=pd.read_csv('final_df.csv',index_col=[0,1])
    return df
#def plt_general(plot,album):

def song_popularity_album():
    """Create a bar chart of each album to answer the question 'which songs are most 
    and least popular per album?
    """    

    #Call the function that will read a csv file and create a dataframe.
    df=read_csv()

    #A numpy array with the values of the first level of MultiIndex.
    albums=np.unique(df.index.get_level_values('Album'))

    for album in albums:
        #Select the row of the DataFrame related to one specific album.
        df_sliced=df.xs(album).sort_values("tracks_popularity", ascending=False)
        
        #The index of the most popular song (wich is the name of the song and the 
        #second level of MultiIndex).
        most_popular=df_sliced["tracks_popularity"].astype(float).idxmax()
        
        #The index of the least popular song (wich is the name of the song and the 
        #second level of MultiIndex).
        least_popular=df_sliced["tracks_popularity"].astype(float).idxmin()

        #The size of the charts.
        plt.figure(figsize=(32,18))

        #Seaborn to make the visualization.
        plot=sns.barplot(data=df_sliced, x="tracks_popularity", y=df_sliced.index,
        palette=set_highlight_palette(df_sliced["tracks_popularity"]))

        #These lines are responsible for setting the labels.
        plot.set_xlabel(xlabel="Popularity", fontsize=30,labelpad=5)
        plot.set_xticklabels(plot.get_xticklabels(), fontsize=24)
        plot.set_ylabel(ylabel="Songs", fontsize=30,labelpad=5)
        plot.set_yticklabels(plot.get_yticklabels(),fontsize=24)

        #Title.
        plt.title(label=f"{album}", loc="center", size=50, pad=10, weight='bold')

        #Footnote.
        plt.figtext(0, 0, f"""The most popular song of {album} is 
{most_popular} and the least is {least_popular}.""", ha="left", fontsize=30, 
bbox={"facecolor": "white", "pad": 10})

        #Save and close the plot.
        plt.savefig(f"imgs/popularity/{album}_popularity.png", bbox_inches='tight')
        plt.close()

def song_duration_album():
    """ Create a bar chart of each album to answer the question 'which songs are 
    longest and which are shortest per album?' """

    #Call the function that will read a csv file and create a dataframe.
    df=read_csv()      

    #A numpy array with the values of the first level of MultiIndex.
    albums=np.unique(df.index.get_level_values('Album'))

    for album in albums:
        #Select the row of the DataFrame related to one specific album.
        df_sliced=df.xs(album).sort_values("tracks_duration", ascending=False)
        
        #The index of the longest song (wich is the name of the song and the 
        #second level of MultiIndex).
        longest=df_sliced["tracks_duration_ms"].astype(float).idxmax()
        
        #The index of the shortest song (wich is the name of the song and the 
        #second level of MultiIndex).
        shortest=df_sliced["tracks_duration_ms"].astype(float).idxmin()

        #The size of the charts.
        plt.figure(figsize=(32,18))

        #Seaborn to make the visualization.
        plot=sns.barplot(data=df_sliced, x="tracks_duration", y=df_sliced.index,
        palette=set_highlight_palette(df_sliced["tracks_duration"]))

        #These lines are responsible for setting the labels.
        plot.set_xlabel(xlabel="Duration (min)", fontsize=30,labelpad=5)
        plot.set_xticklabels(plot.get_xticklabels(), fontsize=24)
        plot.set_ylabel(ylabel="Songs", fontsize=30,labelpad=5)
        plot.set_yticklabels(plot.get_yticklabels(),fontsize=24)
        
        #Title.
        plt.title(label=f"{album}", loc="center", size=50, pad=10, weight='bold')

        #Footnote.
        plt.figtext(0, 0, f"""The longest song of {album} is 
{longest} and the shortest is {shortest}.""", ha="left", fontsize=30, 
bbox={"facecolor": "white", "pad": 10})

        #Save and close the plot.
        plt.savefig(f"imgs/duration/{album}_duration.png",bbox_inches='tight')
        plt.close()

def song_popularity_all_times(n):
    df = read_csv()

    #Set the "Music" level of MultiIndex as index.
    df.index = df.index.get_level_values("Music")
    df=df.sort_values('tracks_popularity', ascending=False)

    #get head and tail of the DF and concat as a new DF
    df_head=df.head(n)
    df_tail=df.tail(n)
    df=pd.concat((df_head,df_tail))
    pal=[]
    for i in range(n):
        pal.append('turquoise')
    for i in range(n):
        pal.append('red')

    plt.figure(figsize=(32,18))
    plot=sns.barplot(data=df, y=df.index, x="tracks_popularity", palette=pal)
    plot.set(ylabel="Popularity", xlabel="Songs")
    plt.figtext(0.895, 0.85, f"{n} Most popular songs all times" , ha="right", fontsize=8)
    plt.figtext(0.589, 0.85, s='             ', bbox={"facecolor": "turquoise", "pad": -10})
    plt.figtext(0.90, 0.795, f"{n} Least popular songs all times" , ha="right", fontsize=8)
    plt.figtext(0.589, 0.80, s='             ', bbox={"facecolor": "red", "pad": -10})
    plt.savefig("imgs/Popularity_all_time.png")
    plt.close()

def song_duration_all_times(n):
    df = read_csv()

    #Set the "Music" level of MultiIndex as index.
    df.index = df.index.get_level_values("Music")
    df=df.sort_values('tracks_duration', ascending=False)

    #get head and tail of the DF and concat as a new DF
    df_head=df.head(n)
    df_tail=df.tail(n)
    df=pd.concat((df_head,df_tail))
    pal=[]
    for i in range(n):
        pal.append('turquoise')
    for i in range(n):
        pal.append('red')

    plt.figure(figsize=(32,18))
    plot=sns.barplot(data=df, y=df.index, x="tracks_duration", palette=pal)
    plot.set_xlabel(xlabel="Songs", fontsize=18)
    plot.set_ylabel(ylabel="Duration", fontsize=18)
    plt.tick_params(labelsize=14)
    plt.figtext(0.895, 0.2, f"{n} Longest songs all times" , ha="right", fontsize=16)
    plt.figtext(0.695, 0.2, s='             ', bbox={"facecolor": "turquoise", "pad": 6})
    plt.figtext(0.90, 0.145, f"{n} Shortest songs all times" , ha="right", fontsize=16)
    plt.figtext(0.695, 0.15, s='             ', bbox={"facecolor": "red", "pad": 6})
    plt.title("""The better and the worst perfoming music 
of The Neighbourhood""",fontweight=1000,fontsize=14, ma='center')
    plt.savefig("imgs/Duration_all_time.png")
    plt.close()



# song_popularity_album()
# song_duration_album()

# song_duration_all_times(7)

# song_popularity_all_times(4)


