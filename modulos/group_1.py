import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import numpy as np
import pandas as pd

sns.set_theme(context="paper", style="darkgrid")

def ms_to_min_sec(ms):
    #Convert miliseconds to minutes.
    minutes = ms / 1000 / 60

    #Get the rest of the previous division.
    seconds = ms / 1000 % 60

    #Convert the minutes and the seconds to int (would be strange to return something
    #like 1.67:45.6, min:sec).
    seconds=int(seconds)
    minutes=int(minutes)

    decimal=list()
    for i in range(0,10):
        decimal.append(i)
  
    #If seconds are less than 10 the return would be something like 4:6 is better if 
    #it's 4:06.  
    if seconds in decimal:
        return float(f"{minutes}.0{seconds}")
    else:
        return float(f"{minutes}.{seconds}")

def df_handling(df):
    #drop all the albums unwanted for the analysis
    new_df=df.drop(labels=['Female Robbery', 'Fallen Star','Middle of Somewhere',
    'Spotify Sessions','Sweater Weather (Young Saab Remix)','Yellow Box',"Daddy Issues (Remix) feat. Syd",
    "Thank You,","Halloween Spooky Hits"], level='Album')

    #Creates a new column using the apply method with the ms_to_min_sec to a previous column
    new_df['tracks_duration']=new_df['tracks_duration_ms'].apply(ms_to_min_sec)

    return new_df

def read_csv():
    #read a csv to create a df
    df=pd.read_csv('../TNBH_Data.csv',index_col=[0,1])

    #does all the needed changes into the df
    df=df_handling(df)

    return df

def set_highlight_palette(column, max_color = 'turquoise', min_color = "red", 
other_color = 'lightgrey'):
    #checks the max and min items in the column.
    max_val = column.max()
    min_val= column.min()
    
    #empty list that will contain the palette.
    pal = []

    #iteration over the column to fill the pal list.
    for item in column:
        if item == max_val:
                pal.append(max_color)
        elif item == min_val:
                pal.append(min_color)
        else:
            pal.append(other_color)
    return pal

def palette_all_songs(n, best="turquoise", worst="red"):
    #empty list 
    pal=list()

    #iteration over a range to fill the pal list 
    for i in range(n):
        pal.append(best)
    for i in range(n):
        pal.append(worst)

    return pal

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
    """_summary_

    :param best_legend: _description_
    :type best_legend: _type_
    :param worst_legend: _description_
    :type worst_legend: _type_
    :param title: _description_
    :type title: _type_
    :param worst_color: _description_, defaults to "red"
    :type worst_color: str, optional
    :param best_color: _description_, defaults to "turquoise"
    :type best_color: str, optional
    """
    if "Longest" in best_legend:
        x_coord=0.689
    else:
        x_coord=0.674
    plt.figtext(0.895, 0.2, best_legend , ha="right", fontsize=36)
    plt.figtext(x_coord, 0.205, s='             ', bbox={"facecolor": best_color, "pad": 10})
    plt.figtext(0.90, 0.145, worst_legend , ha="right", fontsize=36)
    plt.figtext(x_coord, 0.155, s='             ', bbox={"facecolor": worst_color, "pad": 10})
    plt.title(title, weight='bold',fontsize=30, ma='center')

def head_and_tail(df,column,n):
    #Set the "Music" level of MultiIndex as index.
    df.index = df.index.get_level_values("Music")

    #Sort the values with respect to a column
    new_df=df.sort_values(column, ascending=False)

    new_df=new_df.drop_duplicates()


    #get head and tail of the DF and concat as a new DF
    df_head=new_df.head(n)
    df_tail=new_df.tail(n)
    new_df=pd.concat((df_head,df_tail))
    return new_df


def song_popularity_album():
    """Create a bar chart of each album to answer the question 'which songs are most 
    and least popular per album?
    """    

    #Call the function that will read a csv file and create a dataframe with the proper 
    #handling for the analysis.
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
        plt_changes(plot, "Songs", "Popularity", album )

        #Footnote.
        plt.figtext(0, 0, f"""The most popular song of {album} is 
{most_popular} and the least is {least_popular}.""", ha="left", fontsize=30, 
bbox={"facecolor": "white", "pad": 10})

        #Save and close the plot.
        plt.savefig(f"../imgs/popularity/{album}_popularity.png", bbox_inches='tight')
        plt.close()

def song_duration_album():
    """ Create a bar chart of each album to answer the question 'which songs are 
    longest and which are shortest per album?' """

    #Call the function that will read a csv file and create a dataframe with the proper 
    #handling for the analysis.
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
        plt_changes(plot, "Songs", "Duration (min)", album)

        #Footnote.
        plt.figtext(0, 0, f"""The longest song of {album} is 
{longest} and the shortest is {shortest}.""", ha="left", fontsize=30, 
bbox={"facecolor": "white", "pad": 10})

        #Save and close the plot.
        plt.savefig(f"../imgs/duration/{album}_duration.png",bbox_inches='tight')
        plt.close()

def song_popularity_all_times(n):

    #Call the function that will read a csv file and create a dataframe with the proper 
    #handling for the analysis.
    df = read_csv()

    #Creates a new df with the n most/least popular songs
    df_head_tail=head_and_tail(df,"tracks_popularity",n)
    
    #Creates a palette for the chart
    pal=palette_all_songs(n)

    #The size of the figure
    plt.figure(figsize=(32,18))
    #Seaborn to create a plot
    plot=sns.barplot(data=df_head_tail, y=df_head_tail.index, x="tracks_popularity", palette=pal)

    #Variables to be used in the function plt_changes_all_times
    legend_popular="Most popular songs all times"
    legend_not_so_popular="Least popular songs all times"
    title="The better and the worst perfoming songs of The Neighbourhood"

    #functions that make the proper adjusts to labels and other elements of the chart
    plt_changes(plot,"Popularity","Songs")
    plt_changes_all_times(best_legend=legend_popular,worst_legend=legend_not_so_popular, title=title)

    #save and close the figure
    plt.savefig("../imgs/popularity/Popularity_all_time.png", bbox_inches='tight')
    plt.close()

def song_duration_all_times(n):
    #Call the function that will read a csv file and create a dataframe with the proper 
    #handling for the analysis.
    df = read_csv()

    #Creates a new df with the n Logenst/Shortest songs
    df_head_tail=head_and_tail(df, "tracks_duration_ms",n)
    
    #Creates a palette for the chart
    pal=palette_all_songs(n)

    #The size of the figure
    plt.figure(figsize=(32,18))

    #Seabirn to create a plot
    plot=sns.barplot(data=df_head_tail, y=df_head_tail.index, x="tracks_duration", palette=pal)

    #Variables to be used in the function plt_changes_all_times
    legend_long="Longest songs of all times"
    legend_short="Shortest songs of all times"
    title="The better and the worst perfoming songs of The Neighbourhood"

    #functions that make the proper adjusts to labels and other elements of the chart
    plt_changes(plot,"Duration (min)","Songs")
    plt_changes_all_times(best_legend=legend_long,worst_legend=legend_short, title=title)

    #save and close the figure
    plt.savefig("../imgs/duration/Duration_all_time.png", bbox_inches='tight')
    plt.close()



def scatterplot():
    #Call the function that will read a csv file and create a dataframe with the proper 
    #handling for the analysis.
    df=read_csv()

    #Average and correlation rounded
    corr=round(df.corr()['tracks_duration']['tracks_popularity'],2)
    mean=round(df['tracks_popularity'].mean(),1)

    #Creates a PDF object that will allow to save all figures in a single PDF file
    pdf_file=PdfPages('../imgs/Correlation_question_1_6.pdf')

    #The size of the figure
    fig=plt.figure(figsize=(32,18))

    #Seaborn to make the plot
    corr_plot=sns.scatterplot(data=df, y='tracks_duration', x="tracks_popularity")

    #Rectangles that will highlight important sections of the chart.
    rect=mpatches.Rectangle((0,3),100,1.5,alpha=0.1, facecolor='green')
    rect_shorts=mpatches.Rectangle((0,0),48,1.4,alpha=0.1, facecolor='red')

    #Function that make the proper adjusts to labels and other elements of the chart.
    plt_changes(corr_plot,"Popularity","Duration (min)", "Popularity and Duration correlation")

    #Patch that add the rectangles into the figure
    plt.gca().add_patch(rect)
    plt.gca().add_patch(rect_shorts)

    #Save the figure to the pdf and closes it.
    pdf_file.savefig(fig,bbox_inches='tight')
    plt.close()

    #Second figure with a brief discussion about the chart.
    fig2=plt.figure(figsize=(16,9))
    plt.figtext(0.5, 0.9, "A brief review of the visualization", weight='bold', ha='center', fontsize=30)
    plt.figtext(0.05, 0.4, f"""    The Pearson correlation coefficient of the two variables is {corr}, so there is a weak 
correlation between them. It is  possible to see that the  correlation is weak, because
most of the songs are between three and four and a half minutes long, but their popu-
larity ranges from just under 40 to almost 100.
    The correlation, although weak, does exist, as can be seen in the red rectangle whe-
re all the songs with less than a minute and a half have a popularity below the average
({mean}).
    The main conclusions to be drawn are that very short songs should be avoided and
the ideal interval for a song is, in general, 3 to 4 and a half minutes, as this is the length 
of most songs, popular or not.""", ha="left", fontsize=25)
    
    #Save the next page of the pdf and close the figure
    pdf_file.savefig(fig2)
    plt.close()
    #Close the pdf file
    pdf_file.close()



#finalizar coments in all funcs DONE
#commit 
#update min to sec func to be only mins
#update the handling function to eliminate albuns with less than 3 musics  and other things
#check all duration to see if its still right
#make the functios for question 1 and 2 return a pdf with all images for that question
#finish with trys and exceptions
#make the docstring in all functions



