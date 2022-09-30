import requests
from bs4 import BeautifulSoup

def make_request(link):
    """Function that makes request to take the html of a site.

    :param link: Site link.
    :type link: str
    :return: Parsed html of the page.
    :rtype: bs4.BeautifulSoup
    """
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def get_song_links(soup_page):
    """Get all the links of musics in the main page of the artist in the site.

    :param soup_page: Parsed soup page.
    :type soup_page: bs4.BeautifulSoup
    :return: Tuple with songs name and links.
    :rtype: tuple
    """
    song_tags = soup_page.find_all(class_="song-name")
    song_href = []
    song_name = []
    for song_tag in song_tags:
        song_href.append(song_tag["href"])
        song_name.append(song_tag.text)
    return song_name, song_href

def get_songs_data(song_name, song_href):
    """Gets the lyrics and exibihition number of all artist musics.

    :param song_name: List with all the artist song name
    :type song_name: list
    :param song_href: List with all the artist song links
    :type song_href: list
    :return: Dictionary with songs lyrics and exibihition
    :rtype: dict
    """
    songs_data = dict()
    for song_number in range(len(song_name)):
        page = make_request("https://www.letras.mus.br/"+song_href[song_number])
        song_lyrics = page.find(class_="cnt-letra p402_premium").text
        song_exibitions = page.find(class_="cnt-info_exib")
        song_exib_number = song_exibitions.find("b").text
        songs_data[song_name[song_number]] = [song_lyrics, song_exib_number]
    return songs_data

def get_nbhd_songs():
    """Function that takes The Neighbourhood songs data

    :return: The Neighbourhood songs data
    :rtype: dict
    """
    initial_page = make_request("https://www.letras.mus.br/the-neighbourhood/")
    songs_names, songs_hrefs = get_song_links(initial_page)
    return get_songs_data(songs_names, songs_hrefs)