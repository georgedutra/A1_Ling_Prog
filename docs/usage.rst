Usage
=====

.. _installation:

Installation
------------

First install the used libraries using pip:

.. code-block:: console

   $ pip install requirements.txt

.. _scrapping_data:
Scrapping Data
----------------

To retrieve a dictionary with all the artist songs from `SpotifyAPI <https://developer.spotify.com/documentation/web-api/>`_,
you can use the ``spotify_api.get_tracks_data()`` function:

.. autofunction:: spotify_api.get_tracks_data()
   :noindex:
To create a dictionary with all the lyrics from `Letras <https://www.letras.mus.br/the-neighbourhood/>`_, you can use the 
``mus_br_letras.get_nbhd_songs()`` function:

.. autofunction:: mus_br_letras.get_nbhd_songs()
   :noindex:

Finally, if you want to generate a *.csv* so you don't have to do the scrapper all the time, with all the information, you can use
*aqui entra o dataframe* function:

-função-