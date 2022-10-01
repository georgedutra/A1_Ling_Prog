import numpy as np
import pandas as pd
from PIL import Image
import wordcloud as wc
import multidict
import re

def lyrics_all(df: pd.DataFrame) -> str:
    """Receives a DataFrame with musics and returns a string with every lyric concatenated

    :param df: musics DataFrame with one column 'Lyric' that has each music's lyrics as strings
    :type df: pd.DataFrame
    :return: string with every artist's music lyrics concatenated
    :rtype: str
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The function only accepts DataFrames as parameters.")
    
    try:
        lyrics_list = list(df["Lyric"])
        concatenated_string = " ".join(lyrics_list)
    
    except KeyError:
        print("DataFrame has no column 'Lyric'.")
        return ""
    except TypeError:
        print("Some of the lyrics are not strings, and must be changed.")
        return ""
    
    else:
        return concatenated_string

def lyrics_albuns(df: pd.DataFrame) -> dict:
    """Receives a dataframe with musics and return a dictionary with all albums names and all music's lyrics in each album concatenated as a string.

    :param df: Dataframe with an 'Album' Multi-Index (the name of the album each music belongs to), and a 'Lyric' column with each song's lyrics as strings
    :type df: pd.DataFrame
    :return: Dictionary with albums names as keys, and all music's lyrics in each album concatenated as a string, as the key's values.
    :rtype: dict
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The function only accepts DataFrames as parameters.")
    
    try:
        dict_lyrics = {} # Dictionary to be returned in the end
        albums = np.unique(df.index.get_level_values("Album")) # Creates an array with every album's names
        for album_name in albums:
            dict_lyrics[album_name] = lyrics_all(df.xs(album_name))
    
    except KeyError:
        print("DataFrame has no index 'Album'.")
        return {}
    except TypeError:
        print("Some of the album's titles are not strings.")
        return {}
        
    else:
        return dict_lyrics

def music_names(df: pd.DataFrame) -> str:
    """Receives a dataframe with musics and returns a concatenated string with every song's names

    :param df: Dataframe with a Multi-Index called 'Music' (music's name)
    :type df: pd.DataFrame
    :return: string with all musics names concatenated
    :rtype: str
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The function only accepts DataFrames as parameters.")
    try:
        music_list = list(df.index.get_level_values("Music"))
        concat_names = " ".join(music_list)
    except KeyError:
        print("DataFrame has no index 'Music'.")
        return ""
    except TypeError:
        print("Some of the music names are not strings.")
        return ""
    else:    
        return concat_names

def frequency(text: str) -> multidict.MultiDict:
    """Receives a string, and returns a multidict with each word's frequency to create a WordCloud 

    :param text: A string with the text wished to create the WordCloud
    :type text: str
    :return: A Multidict with words as keys and the word's frequencies as values
    :rtype: multidict.MultiDict
    """
    if not isinstance(text, str):
        raise TypeError("The function only accepts strings as parameter")

    # This creates both a MultiDict and a dictionary, because for some reason the WordCloud library asks for it
    frequency_multidict = multidict.MultiDict()
    freq_dict = {}

    # Then, we split the text word by word, and count each ocurrence
    for word in text.split(" "):
        # This regex line excludes common prepositions and articles we don't want to count
        if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", word):
            continue
        appears = freq_dict.get(word, 0)
        freq_dict[word.lower()] = appears + 1

    # Finally, we transfer all the information from the standard dict to the MultiDict, and return it
    for key in freq_dict:
        frequency_multidict.add(key, freq_dict[key])
    return frequency_multidict

def frequency_generator(frequencies: multidict.MultiDict, file_name: str):
    """Receives a frequency MultiDict, and creates a tagcloud named '{file_name}.png'

    :param frequencies: MultiDict with words as keys and frequencies as values
    :type frequencies: multidict.MultiDict
    :param file_name: string that defines the name of the image file to be saved
    :type file_name: str
    """
    if len(frequencies) < 10:
        print(f"The amount of words is insufficient to create the archive {file_name}.png")
        return
    cloud = wc.WordCloud(max_words=10000, max_font_size=40, relative_scaling=0).generate_from_frequencies(frequencies)
    cloud.to_file(f"images/{file_name}.png") 

def generate_cloud_lyrics(df: pd.DataFrame):
    """Receives a DataFrame with musics and generates a TagCloud image named 'all_lyrics_tagcloud.png' according to the most frequent words in all lyrics

    :param df: A DataFrame with a 'Lyric' column, with all music's lyrics as strings
    :type df: pd.DataFrame
    """
    frq_dict = frequency(lyrics_all(df))
    frequency_generator(frq_dict, "all_lyrics_tagcloud")

def generate_cloud_albuns(df: pd.DataFrame):
    """Receives a DataFrame with musics and generates a TagCloud image named '{album_name}_tagcloud.png' according to the most frequent words in each album's lyrics

    :param df: A DataFrame with an index called 'Album' and a 'Lyric' column, with all music's lyrics as strings
    :type df: pd.DataFrame
    """
    # Picks a dictionary with each album's lyrics, and generate a tagcloud for each album
    albuns = lyrics_albuns(df)
    for key in albuns:
        frq_dict = frequency(albuns[key])
        frequency_generator(frq_dict, f"{key}_tagcloud") 

def generate_cloud_music_names(df: pd.DataFrame):
    """Receives a DataFrame with musics and generates a TagCloud image named 'names_tagcloud.png' according to the most frequent words in all music's titles

    :param df: A DataFrame with an index called 'Name', with all music's names as strings
    :type df: pd.DataFrame
    """
    frq_dict = frequency(music_names(df))
    frequency_generator(frq_dict, "names_tagcloud")

####################################################################################################################
# creating a fiction dataframe while I dont have the oficial one
album = ["Album 1","Album 1","Album 2","Album 2"]
names = ["Daddy Issues", "ABC", "DEF", "GHI"]
indexes = pd.MultiIndex.from_arrays([album, names], names=("Album", "Music"))
columns = ["Released", "Popularity", "Lyric"]

dados = [[1982, 2600000, "in hac habitasse. Nec ullamcorper sit amet risus. Consectetur libero id faucibus nisl tincidunt eget. Elit pellentesque habitant morbi tristique senectus et netus."], 
[2000,100000,"Leberkas buffalo beef ribs, drumstick pastrami doner pork belly pork loin corned beef short ribs. Brisket tail rump ribeye jerky, ham hock chicken cow salami ham leberkas picanha. Alcatra spare ribs boudin pig. Strip steak cow andouille doner corned beef t-bone pancetta short ribs landjaeger salami boudin pork chop shoulder beef ribs tail. Porchetta shankle short ribs t-bone buffalo, beef ribs hamburger brisket chicken. Meatball turkey alcatra t-bone pork, ribeye biltong. Chislic ham flank jowl, porchetta beef ribs bresaola pork ham hock venison t-bone chicken. Alcatra tenderloin jowl sausage cupim, meatloaf prosciutto strip steak. Flank tail kielbasa bacon capicola drumstick turducken shankle burgdoggen filet mignon. Bacon alcatra chislic, beef ribs venison leberkas salami cow ham hock buffalo ball tip hamburger biltong corned beef tenderloin. Short ribs pastrami pork loin, landjaeger buffalo pancetta ribeye. Pancetta rump pork belly ground round bacon leberkas salami hamburger spare ribs jerky. Shoulder burgdoggen fatback filet mignon pork chop leberkas spare ribs short ribs pig boudin corned beef beef capicola buffalo pork loin. Pork loin ham tail, short ribs jowl porchetta t-bone cupim kevin. Drumstick meatball leberkas, tail burgdoggen pancetta ham hock flank pig chicken filet mignon salami t-bone. Brisket frankfurter meatball, short ribs jerky chicken spare ribs. Spare ribs beef capicola, short loin strip steak t-bone flank cow. Buffalo alcatra cow, short loin filet mignon ham venison ribeye short ribs salami turducken corned beef pig."],
[2007,600000,"Beef flank short loin kevin, shoulder ground round pork chop. Sausage tenderloin picanha pig rump burgdoggen. Shoulder ribeye corned beef, turducken prosciutto short ribs pork belly ball tip landjaeger. Turkey bresaola meatball beef ribs chuck hamburger sausage chislic. Sirloin picanha pancetta leberkas shank boudin. Bresaola brisket pastrami chicken. Jerky tri-tip tenderloin picanha. Short ribs kevin flank, tenderloin landjaeger buffalo salami meatloaf swine. Bacon landjaeger sirloin pork loin. Drumstick ham hock shoulder turducken alcatra rump tongue tenderloin doner beef ribs bresaola. Pancetta tri-tip ham hock pork chop. Turducken ball tip ham beef ribs tongue pancetta shank drumstick, spare ribs venison kevin tail boudin salami jowl. Meatball pork belly tongue tenderloin hamburger. Ball tip spare ribs pork chop pastrami short ribs cow pig ribeye rump buffalo beef. Beef flank turkey chislic, alcatra shankle ground round shoulder boudin strip steak buffalo short ribs ham hock. Pastrami filet mignon spare ribs rump chislic pork bresaola doner corned beef. Corned beef jerky doner alcatra pastrami ground round. Spare ribs turkey biltong cupim ground round pastrami jowl chuck pancetta prosciutto picanha. Alcatra drumstick tail picanha, pork belly brisket pancetta tenderloin ribeye beef pastrami."],
[2016,3000000,"Spicy jalapeno bacon ipsum dolor amet sausage chislic venison, chicken tri-tip pork leberkas buffalo frankfurter beef ribs andouille sirloin rump. Pastrami pork belly swine tail tri-tip. Ground round spare ribs shoulder brisket burgdoggen. Tongue tri-tip venison pork. Pig beef turkey, bacon chuck buffalo short ribs salami cupim picanha cow kielbasa. Shoulder swine leberkas, chicken ball tip ribeye t-bone. Pork andouille flank, frankfurter tenderloin corned beef jerky ball tip fatback prosciutto ribeye drumstick. Bacon picanha prosciutto buffalo venison meatball tri-tip kielbasa landjaeger. Swine capicola pork loin, porchetta salami leberkas corned beef shankle. Landjaeger short ribs fatback tail, meatball swine chuck drumstick kevin ham spare ribs beef bresaola pork belly strip steak. Kevin swine pastrami spare ribs landjaeger. Flank pastrami jowl turducken meatloaf turkey shank filet mignon alcatra andouille short loin fatback sausage doner tongue. Turkey alcatra ball tip tenderloin doner. Landjaeger bacon shankle pork drumstick ham turkey bresaola, cupim boudin kielbasa."]]

df = pd.DataFrame(dados, index=indexes, columns=columns)

generate_cloud_music_names(df)