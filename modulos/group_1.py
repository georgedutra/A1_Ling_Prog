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

def ms_to_min(ms):
    """A simple millisecond to min converter.

    :param ms: The number of Miliseconds to be converted
    :type ms: Int
    :return: The number of minutes.
    :rtype: Float
    """    
    minutes = ms / 1000 / 60
    return minutes

def df_handling(df, identifier):
    """This function handles the Dataframe by dropping the unwanted albums and 
    creating a column for the duration in minutes.

    :param df: A dataFrame
    :type df: pandas.core.frame.DataFrame
    :param identifier: An identifier used to select what albuns will not be in the analysis
    :type identifier: str
    :return: A dataframe handled
    :rtype: pandas.core.frame.DataFrame
    """    
    
    #A list of all the unwanted albums
    if identifier == 'Albums':
        albums_drop=['Female Robbery', 'Fallen Star',"batata",'Middle of Somewhere',
    'Spotify Sessions','Sweater Weather (Young Saab Remix)','Yellow Box',"Daddy Issues (Remix) feat. Syd",
    "Thank You,","Halloween Spooky Hits"]
    else:
        albums_drop=["Halloween Spooky Hits"]

    new_df=df.copy(deep=True)
    #drop all the albums unwanted for the analysis
    for album in albums_drop:
        try:
            new_df=new_df.drop(labels=album, level='Album')
        except KeyError:
            pass
    #Creates a new column using the apply method with the ms_to_min to a previous column
    new_df['tracks_duration']=new_df['tracks_duration_ms'].apply(ms_to_min)

    return new_df

def handled_df(identifier=""):
    """Creates a dataframe from a csv to be handled.

    :param identifier: An identifier used to select what albuns will not be in the analysis, defaults to ""
    :type identifier: str, optional
    :return: The handled df that will be used in the questions.
    :rtype: pandas.core.frame.DataFrama
    """    

    #read a csv to create a df
    df=pd.read_csv('TNBH_Data.csv',index_col=[0,1])

    #does all the needed changes into the df
    df=df_handling(df,identifier)

    return df

def set_highlight_palette(column, max_color = 'turquoise', min_color = "red", 
other_color = 'lightgrey'):
    """Creats a list to use as palette to highlight the max and min of each case in the questions 1 
    and 2.

    :param column: The column
    :type column: pandas.core.series.Series
    :param max_color: A color to represent the max of the series, defaults to 'turquoise'
    :type max_color: str, optional
    :param min_color: A color to represent the min of the series, defaults to "red"
    :type min_color: str, optional
    :param other_color: a color to represent all other elements of the series, defaults to 'lightgrey'
    :type other_color: str, optional
    :return: A list that will be used as palette
    :rtype: list
    """

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
    """Creats a list to use as palette to highlight the n-max and n-min of each case 
    in the questions 3 and 4.

    :param n: The integer to be used as the number of max's and min's 
    :type n: int
    :param best: The color to represent the max's, defaults to "turquoise"
    :type best: str, optional
    :param worst: The color to represent the min's, defaults to "red"
    :type worst: str, optional
    :return: A list what will be used as palette.
    :rtype: list
    """    
    
    #empty list
    pal=list()

    #iteration over a range to fill the pal list 
    for i in range(n):
        pal.append(best)
    for i in range(n):
        pal.append(worst)

    return pal

def plt_changes(plot,x_label,y_label,album=''):
    """Make changes on the plots for all questions

    :param plot: The plot that will receive the changes.
    :type plot: matplotlib.axes._subplots.AxesSubplot
    :param x_label: The label to be used on the x-axis
    :type x_label: str
    :param y_label: The label to be used on the y-axis
    :type y_label: str
    :param album: The name of the album to used as title of the chart, defaults to ''
    :type album: str, optional
    """    

    #These lines are responsible for setting the labels.
    plot.set_xlabel(xlabel=x_label, fontsize=30,labelpad=5)
    plot.set_xticklabels(plot.get_xticklabels(), fontsize=24)
    plot.set_ylabel(ylabel=y_label, fontsize=30,labelpad=5)
    plot.set_yticklabels(plot.get_yticklabels(),fontsize=24)
    
    #Title.
    plt.title(label=f"{album}", loc="center", size=50, pad=10, weight='bold')



def plt_changes_all_times( best_legend, worst_legend, title,
worst_color="red", best_color="turquoise"):
    """Make especial changes on the plot of questions 3 and 4.

    :param best_legend: A string to be used in the legend to represet the longest/most popular songs
    :type best_legend: str
    :param worst_legend: A string to be used in the legend to represet the shortest/least popular songs
    :type worst_legend: str
    :param title: The title of the chart
    :type title: str
    :param worst_color: The color to represent the shortest/least popular songs in the legend, defaults to "red"
    :type worst_color: str, optional
    :param best_color: The color to represent the shortest/least popular songs in the legend, defaults to "turquoise"
    :type best_color: str, optional
    """
    #To make the legends look good in both cases
    if "Longest" in best_legend:
        x_coord=0.689
    else:
        x_coord=0.674

    #Just to make a small legend for the chart
    plt.figtext(0.895, 0.2, best_legend , ha="right", fontsize=36)
    plt.figtext(x_coord, 0.205, s='             ', bbox={"facecolor": best_color, "pad": 10})
    plt.figtext(0.90, 0.145, worst_legend , ha="right", fontsize=36)
    plt.figtext(x_coord, 0.155, s='             ', bbox={"facecolor": worst_color, "pad": 10})
    plt.title(title, weight='bold',fontsize=30, ma='center')

def drop_duplicated_songs(df):
    """Drops all the songs that repeat throughout the albums.

    :param df: a df with repeated indexes on a level of MultiIndex
    :type df: pandas.core.frame.DataFrame
    :return: a df without the repeated indexes
    :rtype: pandas.core.frame.DataFrame
    """    
    #drop all the music that repeat into diferent albuns
    new_df=df.copy(deep=True)
    new_df.index = df.index.get_level_values("Music")
    new_df = df[~df.index.duplicated(keep='first')]
    return new_df

def head_and_tail(df,column,n):
    """Creates a new_df with the head and tail of the df sorted.

    :param df: A df that will be ordered and then sliced
    :type df: pandas.core.frame.DataFrame
    :param column: A string thats is used to know from where the function is being called
    :type column: str
    :param n: a number to be used as parameter for the head and tail method from pandas
    :type n: int
    :return: A new_df with n items from the head and n items from the tail 
    :rtype: pandas.core.frame.DataFrame
    """    
    #Set the "Music" level of MultiIndex as index.
    df.index = df.index.get_level_values("Music")

    #Sort the values with respect to a column
    new_df=df.sort_values(column, ascending=False)

    #if the function is being called from song_duration_all_time() drop the repeated songs
    if column == "tracks_duration_ms":
        new_df=drop_duplicated_songs(new_df)


    #get head and tail of the DF and concat as a new DF
    df_head=new_df.head(n)
    df_tail=new_df.tail(n)
    new_df=pd.concat((df_head,df_tail))
    return new_df


def song_popularity_album(df):
    """Create a pdf file with bar charts for each album to answer the question 'which songs are the most 
    and least popular per album?
    :param df: A handled df to used in the answer.
    :type df: pandas.core.frame.DataFrame.
    """    

    #Creates a pdf object that will allow to save all figures in a single pdf file.
    pdf_file=PdfPages("images\Popularity_per_album.pdf")

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
        fig=plt.figure(figsize=(32,18))

        #Seaborn to make the visualization.
        plot=sns.barplot(data=df_sliced, x="tracks_popularity", y=df_sliced.index,
        palette=set_highlight_palette(df_sliced["tracks_popularity"]))

        #Make plt changes.
        plt_changes(plot, "Songs", "Popularity", album )

        #Footnote.
        plt.figtext(0, 0, f"""The most popular song of {album} is 
{most_popular} and the least is {least_popular}.""", ha="left", fontsize=30, 
bbox={"facecolor": "white", "pad": 10})

        #Save a figure to the pdf and close the plot
        pdf_file.savefig(fig, bbox_inches='tight')
        plt.close()
    #Close the pdf file
    pdf_file.close()

def song_duration_album(df):
    """ Create pdf file with bar charts for each album to answer the question 'which songs are 
    longest and which are shortest per album?' 

    :param df: A handled df to used in the answer.
    :type df: pandas.core.frame.DataFrame.
    """

    #Creates a pdf object that will allow to save all figures in a single pdf file.
    pdf_file=PdfPages("images/Duration_per_album.pdf")

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
        fig=plt.figure(figsize=(32,18))

        #Seaborn to make the visualization.
        plot=sns.barplot(data=df_sliced, x="tracks_duration", y=df_sliced.index,
        palette=set_highlight_palette(df_sliced["tracks_duration"]))

        #Make plt changes
        plt_changes(plot, "Duration (min)","Songs", album)

        #Footnote.
        plt.figtext(0, 0, f"""The longest song of {album} is 
{longest} and the shortest is {shortest}.""", ha="left", fontsize=30, 
bbox={"facecolor": "white", "pad": 10})

        #Save a figure to the pdf and close the plot.
        pdf_file.savefig(fig,bbox_inches='tight')
        plt.close()
    #Close the pdf file
    pdf_file.close()

def song_popularity_all_times(df,n):
    """Creates a bar chart with the n-most and n-least popular song of all times.

    :param df: A handled df to used in the answer.
    :type df: pandas.core.frame.DataFrame.
    :param n: How much elements for most/least popular to be plotted in the chart.
    :type n: int
    """    

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
    plt.savefig("images/Popularity_all_time.pdf", bbox_inches='tight')
    plt.close()

def song_duration_all_times(df,n):
    """Creates a bar chart with the n-longest and n-shortest popular song of all times.

    :param df: A handled df to used in the answer.
    :type df: pandas.core.frame.DataFrame.
    :param n: How much elements for longest/shortest to be plotted in the chart.
    :type n: int
    """    

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
    title="The longest and the shortest songs of The Neighbourhood"

    #functions that make the proper adjusts to labels and other elements of the chart
    plt_changes(plot,"Duration (min)","Songs")
    plt_changes_all_times(best_legend=legend_long,worst_legend=legend_short, title=title)

    #save and close the figure
    plt.savefig("images/Duration_all_time.pdf", bbox_inches='tight')
    plt.close()



def scatterplot(df):
    """
    Creates a scatterplot to visualize any correlations between the popularity and the duration of the musics.
    :param df: A handled df to used in the answer.
    :type df: pandas.core.frame.DataFrame.
    """    

    #Call the function that will read a csv file and create a dataframe with the proper 
    #handling for the analysis.

    #Average and correlation rounded
    corr=round(df.corr()['tracks_duration']['tracks_popularity'],2)
    mean=round(df['tracks_popularity'].mean(),1)

    #Creates a PDF object that will allow to save all figures in a single PDF file
    pdf_file=PdfPages('images/Correlation_duration_popularity.pdf')

    #The size of the figure
    fig=plt.figure(figsize=(32,18))

    #Seaborn to make the plot
    corr_plot=sns.scatterplot(data=df, y='tracks_duration', x="tracks_popularity", s=100)

    #Rectangles that will highlight important sections of the chart.
    rect=mpatches.Rectangle((0,3),100,1.5,alpha=0.1, facecolor='green')
    rect_shorts=mpatches.Rectangle((0,0),48,1.5,alpha=0.1, facecolor='red')

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




#update the handling function to eliminate albuns with less than 3 musics  and other things
#finish with trys and exceptions

# df_albums=handled_df('Albums')
# df=handled_df()

# song_duration_album(df_albums)
# song_popularity_album(df_albums)
# song_duration_all_times(df,4)
# song_popularity_all_times(df,4)
# scatterplot(df)


