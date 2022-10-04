import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

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

def palette_all_songs(n, best="turquoise", worst="red"):
    pal=list()
    for i in range(n):
        pal.append(best)
    for i in range(n):
        pal.append(worst)
    return pal

def read_csv():
    df=pd.read_csv('final_df.csv',index_col=[0,1])
    return df


def plt_changes(plot,x_label,y_label,album=''):

    #These lines are responsible for setting the labels.
    plot.set_xlabel(xlabel=x_label, fontsize=30,labelpad=5)
    plot.set_xticklabels(plot.get_xticklabels(), fontsize=24)
    plot.set_ylabel(ylabel=y_label, fontsize=30,labelpad=5)
    plot.set_yticklabels(plot.get_yticklabels(),fontsize=24)
    
    #Title.
    plt.title(label=f"{album}", loc="center", size=50, pad=10, weight='bold')



def plt_changes_all_times( best_legend, worst_legend, title,
worst_color="red", best_color="turquoise"):
    plt.figtext(0.895, 0.2, best_legend , ha="right", fontsize=36)
    plt.figtext(0.6895, 0.205, s='             ', bbox={"facecolor": best_color, "pad": 10})
    plt.figtext(0.90, 0.145, worst_legend , ha="right", fontsize=36)
    plt.figtext(0.6895, 0.155, s='             ', bbox={"facecolor": worst_color, "pad": 10})
    plt.title(title, weight='bold',fontsize=30, ma='center')




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

        #Make plt changes 
        plt_changes(plot, album, "Popularity", "Songs")

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

        #Make plt changes
        plt_changes(plot,album,"Duration (min)", "Songs")

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
    
    #Creates a palette for the chart
    pal=palette_all_songs(n)


    plt.figure(figsize=(32,18))
    plot=sns.barplot(data=df, y=df.index, x="tracks_popularity", palette=pal)

    legend_long="Most popular songs all times"
    legend_short="Least popular songs all times"
    title="The better and the worst perfoming songs of The Neighbourhood"

    plt_changes(plot,"Popularity","Songs")
    plt_changes_all_times(best_legend=legend_long,worst_legend=legend_short, title=title)

    plt.savefig("imgs/Popularity_all_time.png", bbox_inches='tight')
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
    
    #Creates a palette for the chart
    pal=palette_all_songs(n)

    plt.figure(figsize=(32,18))
    plot=sns.barplot(data=df, y=df.index, x="tracks_duration", palette=pal)

    legend_long="Longest songs of all times"
    legend_short="Shortest songs of all times"
    title="The better and the worst perfoming songs of The Neighbourhood"

    plt_changes(plot,"Duration (min)","Songs")
    plt_changes_all_times(best_legend=legend_long,worst_legend=legend_short, title=title)

    plt.savefig("imgs/Duration_all_time.png", bbox_inches='tight')
    plt.close()



#song_popularity_album()
# song_duration_album()

song_duration_all_times(7)

song_popularity_all_times(2)


