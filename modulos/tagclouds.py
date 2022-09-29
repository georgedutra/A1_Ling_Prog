import numpy as np
import pandas as pd
from PIL import Image
import wordcloud as wc
import multidict
import re
from scipy.ndimage import gaussian_gradient_magnitude
import matplotlib.pyplot as plt
import random

def lyrics_all(df):
    """Receives a DataFrame with musics and returns a string with every lyric concatenated

    :param df: musics DataFrame with one column 'Lyric' that has each music's lyrics as strings
    :type df: pandas.DataFrame
    :return: string with every artist's music lyrics concatenated
    :rtype: str
    """
    lyrics_list = list(df["Lyric"])
    concatenated_string = " ".join(lyrics_list)
    return concatenated_string

def lyrics_albuns(df):
    """Receives a dataframe with musics and return a dictionary with all albums names and all music's lyrics in each album concatenated as a string.

    :param df: Dataframe with an 'Album' Multi-Index (the name of the album each music belongs to), and a 'Lyric' column with each song's lyrics as strings
    :type df: pandas.DataFrame
    :return: Dictionary with albums names as keys, and all music's lyrics in each album concatenated as a string, as the key's values.
    :rtype: dict
    """

    dict_lyrics = {} # Dictionary to be returned in the end
    albums = np.unique(df.index.get_level_values("Album")) # Creates an array with every album's names
    for album_name in albums:
        dict_lyrics[album_name] = lyrics_concat(df.xs(album_name))
    return dict_lyrics

def music_names(df):
    """Receives a dataframe with musics and returns a concatenated string with every song's names

    :param df: Dataframe with a Multi-Index called 'Music' (music's name)
    :type df: pandas.DataFrame
    :return: string with all musics names concatenated
    :rtype: str
    """
    music_list = list(df.index.get_level_values("Music"))
    concat_names = " ".join(music_list)
    return concat_names

def frequency(text):
    """Receives a string, and returns a multidict with each word's frequency to create a WordCloud 

    :param text: A string with the text wished to create the WordCloud
    :type text: str
    :return: A Multidict with words as keys and the word's frequencies as values
    :rtype: multidict.MultiDict
    """
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

def cloud_parameters(image, low_quality=False, no_white=False):
    """Receives an image's path, and return important masking parameters for the WordCloud

    :param image: Path to the image that will be used to create the TagCloud
    :type image: str
    :param low_quality: Reduces the quality of the final image in case the script becomes too slow, defaults to False
    :type low_quality: bool, optional
    :param no_white: Excludes white parts from the mask, defaults to False
    :type no_white: bool, optional
    :return: Parameters colors, mask and edge map
    :rtype: tuple
    """
    # First, we pick the image as an array 
    colors = np.array(Image.open(image))
    if low_quality == True:
        colors = colors[::3, ::3] 

    # Then, we take a copy of the image to use as mask
    mask = colors.copy()
    if no_white == True:
        mask[mask.sum() == 0] = 255 

    return colors, mask

def cloud_all_lyrics(df):
    """Receives a DataFrame with music lyrics, and create a TagCloud with all lyrics words according to frequency.

    :param df: pandas DataFrame with at least one column called 'Lyric', with each music's lyrics in it
    :type df: pandas.DataFrame
    """
    # Lets pick the standard parameters for the wordcloud
    colors, mask = cloud_parameters("images/band_logo.png")

    # Thus, let's pick the frequency dictionary to plot the TagCloud
    text = frequency(lyrics_all(df))

    # Then, we plot and generate the TagCloud using the parameters
    cloud = wc.WordCloud(background_color="black" , max_words=20000, mask=mask, max_font_size=40, relative_scaling=0, contour_width=1,contour_color="white")
    cloud.generate_from_frequencies(text)
    
    # Finally, we recolor the words and save it
    cloud_colors = wc.ImageColorGenerator(colors)
    cloud.recolor(color_func=cloud_colors)
    cloud.to_file("images/all_lyrics_tagcloud.png")


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

# cloud_all_lyrics(df)

