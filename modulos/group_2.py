import numpy as np
import pandas as pd
from tagclouds import frequency, lyrics_all, lyrics_albuns, music_names
import multidict

# Grupo de Perguntas 2:

# Quais são as palavras mais comuns nos títulos dos Álbuns?
# Quais são as palavras mais comuns nos títulos das músicas?
# Quais são as palavras mais comuns nas letras das músicas, por Álbum?
# Quais são as palavras mais comuns nas letras das músicas, em toda a discografia?
# O título de um álbum é tema recorrente nas letras?
# O título de uma música é tema recorrente nas letras?

def dict_to_series(dict: dict | multidict.MultiDict) -> pd.Series:
    """Receives a dictionary with words and frequency numbers and returns a Series object sorted by descending values

    :param dict: Dictionary with words as keys and numbers as values
    :type dict: dict | multidict.MultiDict
    :return: Pandas Series with words as keys and numbers as values, sorted by descending values
    :rtype: pd.Series
    """
    indexes = dict.keys()
    values = dict.values()
    series = pd.Series(values, indexes)
    return series.sort_values(ascending=False)

def question_1(df: pd.DataFrame):
    """Receives a DataFrame with musics information and print at the console wich words are the most common among the band's album's titles 

    :param df: DataFrame with one MultiIndex named 'Album' with the band's album's names as strings
    :type df: pd.DataFrame
    """
    try:
        albums = np.unique(df.index.get_level_values("Album"))
        albums_string = " ".join(albums)
        albums_series = dict_to_series(frequency(albums_string))
    except KeyError as error:
        print(f"{error}, DataFrame must have an index named 'Album' for question 1.")
    else:
        print("\nThe most common words in the band's album's titles are:\n", albums_series[0:5].index.values, "\n\n", "="*60, sep="")

def question_2(df: pd.DataFrame):
    """Receives a DataFrame with musics information and print at the console wich words are the most common among the band's music's titles 

    :param df: DataFrame with one MultiIndex named 'Music' with the band's music's names as strings
    :type df: pd.DataFrame
    """
    try:
        titles_series = dict_to_series(frequency(music_names(df)))
    except KeyError as error:
        print(f"{error}, DataFrame must have an index named 'Music' for question 2.")
    else:
        print("\nThe most common words in the band's music's titles are:\n", titles_series[0:5].index.values, "\n\n","="*60, sep="")

def question_3(df: pd.DataFrame):
    """Receives a DataFrame with musics information and print at the console wich words are the most common among each album's music's lyrics 

    :param df: DataFrame with one MultiIndex named 'Album' and one column named 'Lyric' with the band's music's lyrics as strings
    :type df: pd.DataFrame
    """
    try:
        lyrics = lyrics_albuns(df)

        for album in lyrics:
            words_freq = dict_to_series(frequency(lyrics[album]))
            print(f"\nThe most common words in the lyrics from the album {album} are:\n", words_freq[0:5].index.values,"\n\n","="*60, sep="")
    except KeyError as error:
        print(f"{error}, DataFrame must have an index named 'Album' and a column named 'Lyric' for question .")
        
def question_4(df: pd.DataFrame):
    """Receives a DataFrame with musics information and print at the console wich words are the most common among all music's lyrics 

    :param df: DataFrame with one column named 'Lyric' with the band's music's lyrics as strings
    :type df: pd.DataFrame
    """
    try:
        lyrics_freq = dict_to_series(frequency(lyrics_all(df)))
    except KeyError as error:
        print(f"{error}, DataFrame must have a column named 'Lyric' for question 4.")
    else:
        print("\nThe most common words in the lyrics from the whole band's discography are:\n", lyrics_freq[0:5].index.values, "\n\n","="*60, sep="")

def question_5(df: pd.DataFrame):
    """Receives a DataFrame with musics information and verify if at least half the albums have it's titles in some of it's music's lyrics  

    :param df: DataFrame with one MultiIndex named 'Album' and one column named 'Lyric' with the band's music's lyrics as strings
    :type df: pd.DataFrame
    """
    try:
        lyrics = lyrics_albuns(df)
        ocurrencies = 0
    
        for album in lyrics:
            if album in lyrics[album]:
                ocurrencies += 1
    except KeyError as error:
        print(f"{error}, DataFrame must have an index named 'Album' and one column named 'Lyric' for question 5.")
    else:
        if ocurrencies >= (len(lyrics)/2):
            print("\nThis band's musics usually have the album's titles into it's lyrics!\n\n", "="*60,sep="")
        else:
            print("\nThis band's musics usually don't have the album's titles into it's lyrics.\n\n", "="*60,sep="")

def question_6(df: pd.DataFrame):
    """Receives a DataFrame with musics information and verify if at least half the musics have it's titles in it's own lyrics  

    :param df: DataFrame with one MultiIndex named 'Music' and one column named 'Lyric' with the band's music's lyrics as strings
    :type df: pd.DataFrame
    """
    try:
        music_list = list(df.index.get_level_values("Music"))
        ocurrencies = 0

        for music in music_list:
            music_df = df.xs(music, level="Music")
            if music in music_df.iloc[0]["Lyric"]:
                ocurrencies += 1
    except KeyError as error:
        print(f"{error}, DataFrame must have an index named 'Music' and one column named 'Lyric' for question 6.")
    else:
        if ocurrencies >= (len(music_list)/2):
            print("\nThis band's musics usually have the music's title into it's lyrics!\n\n", "="*60,sep="")
        else:
            print("\nThis band's musics usually don't have the music's titles into it's lyrics.\n\n", "="*60,sep="")


##################################################################################################
# Outro dataframe de teste enquanto não tenho o final para testar

album = ["Album 1","Album 1","Album 2","Album 2"]
names = ["Daddy Issues", "ABC", "DEF", "GHI"]
indexes = pd.MultiIndex.from_arrays([album, names], names=("Album", "Music"))
columns = ["Released", "Popularity", "Lyric"]
dados = [[1982, 2600000, "in Daddy Issues hac habitasse. Nec ullamcorper sit amet risus. Consectetur libero id faucibus nisl tincidunt eget. Elit pellentesque habitant morbi tristique senectus et netus."], 
[2000,100000,"Leberkas buffalo ABC Album 1 beef ribs, drumstick pastrami doner pork belly pork loin corned beef short ribs. Brisket tail rump ribeye jerky, ham hock chicken cow salami ham leberkas picanha. Alcatra spare ribs boudin pig. Strip steak cow andouille doner corned beef t-bone pancetta short ribs landjaeger salami boudin pork chop shoulder beef ribs tail. Porchetta shankle short ribs t-bone buffalo, beef ribs hamburger brisket chicken. Meatball turkey alcatra t-bone pork, ribeye biltong. Chislic ham flank jowl, porchetta beef ribs bresaola pork ham hock venison t-bone chicken. Alcatra tenderloin jowl sausage cupim, meatloaf prosciutto strip steak. Flank tail kielbasa bacon capicola drumstick turducken shankle burgdoggen filet mignon. Bacon alcatra chislic, beef ribs venison leberkas salami cow ham hock buffalo ball tip hamburger biltong corned beef tenderloin. Short ribs pastrami pork loin, landjaeger buffalo pancetta ribeye. Pancetta rump pork belly ground round bacon leberkas salami hamburger spare ribs jerky. Shoulder burgdoggen fatback filet mignon pork chop leberkas spare ribs short ribs pig boudin corned beef beef capicola buffalo pork loin. Pork loin ham tail, short ribs jowl porchetta t-bone cupim kevin. Drumstick meatball leberkas, tail burgdoggen pancetta ham hock flank pig chicken filet mignon salami t-bone. Brisket frankfurter meatball, short ribs jerky chicken spare ribs. Spare ribs beef capicola, short loin strip steak t-bone flank cow. Buffalo alcatra cow, short loin filet mignon ham venison ribeye short ribs salami turducken corned beef pig."],
[2007,600000,"Beef flank short loin kevin, shoulder ground round pork chop. Sausage tenderloin picanha pig rump burgdoggen. Shoulder ribeye corned DEF beef, turducken prosciutto short ribs pork belly ball tip landjaeger. Turkey bresaola meatball beef ribs chuck hamburger sausage chislic. Sirloin picanha pancetta leberkas shank boudin. Bresaola brisket pastrami chicken. Jerky tri-tip Album 2 tenderloin picanha. Short ribs kevin flank, tenderloin landjaeger buffalo salami meatloaf swine. Bacon landjaeger sirloin pork loin. Drumstick ham hock shoulder turducken alcatra rump tongue tenderloin doner beef ribs bresaola. Pancetta tri-tip ham hock pork chop. Turducken ball tip ham beef ribs tongue pancetta shank drumstick, spare ribs venison kevin tail boudin salami jowl. Meatball pork belly tongue tenderloin hamburger. Ball tip spare ribs pork chop pastrami short ribs cow pig ribeye rump buffalo beef. Beef flank turkey chislic, alcatra shankle ground round shoulder boudin strip steak buffalo short ribs ham hock. Pastrami filet mignon spare ribs rump chislic pork bresaola doner corned beef. Corned beef jerky doner alcatra pastrami ground round. Spare ribs turkey biltong cupim ground round pastrami jowl chuck pancetta prosciutto picanha. Alcatra drumstick tail picanha, pork belly brisket pancetta tenderloin ribeye beef pastrami."],
[2016,3000000,"Spicy jalapeno bacon GHI ipsum dolor amet sausage chislic venison, chicken tri-tip pork leberkas buffalo frankfurter beef ribs andouille sirloin rump. Pastrami pork belly swine tail tri-tip. Ground round spare ribs shoulder brisket burgdoggen. Tongue tri-tip venison pork. Pig beef turkey, bacon chuck buffalo short ribs salami cupim picanha cow kielbasa. Shoulder swine leberkas, chicken ball tip ribeye t-bone. Pork andouille flank, frankfurter tenderloin corned beef jerky ball tip fatback prosciutto ribeye drumstick. Bacon picanha prosciutto buffalo venison meatball tri-tip kielbasa landjaeger. Swine capicola pork loin, porchetta salami leberkas corned beef shankle. Landjaeger short ribs fatback tail, meatball swine chuck drumstick kevin ham spare ribs beef bresaola pork belly strip Album 2 steak. Kevin swine pastrami spare ribs landjaeger. Flank pastrami jowl turducken meatloaf turkey shank filet mignon alcatra andouille short loin fatback sausage doner tongue. Turkey alcatra ball tip tenderloin doner. Landjaeger bacon shankle pork drumstick ham turkey bresaola, cupim boudin kielbasa."]]

df = pd.DataFrame(dados, index=indexes, columns=columns)

question_1(df)
question_2(df)
question_3(df)
question_4(df)
question_5(df)
question_6(df)