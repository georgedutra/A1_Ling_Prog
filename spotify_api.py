import requests
import datetime
from urllib.parse import urlencode
import base64

class SpotifyAPI(object):
    """Classe que define o objeto de busca na API do spotify. Reúne todas as funções referentes as requisições feitas ao servirdor do Spotify.

    :param object: _description_
    :type object: _type_
    :raises Exception: _description_
    :return: _description_
    :rtype: _type_
    """
    
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, *args, **kwargs):
        """Função de inicialização do objeto. Já acessa o cliente criado para a atividade proposta da A1.
        """
        super().__init__(*args, **kwargs)
        self.client_id = "28afa3960a524b87943dc0426a022a3e"
        self.client_secret = "6fbdae782c3440c28835590d9146b00f"
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
        
    def get_resource(self, lookup_id, resource_type, version='v1', extra=""):
        """Função que busca o endpoint da api, fazendo as requisições baseadas nos parametros passados.

        :param lookup_id: ID que está sendo buscado. Representa o ID do tipo que está sendo requerido.
        :type lookup_id: str
        :param resource_type: Tipo do que está sendo buscado, artista, musica ou album no nosso caso.
        :type resource_type: str
        :param version: Versao da API sendo utilizada, por padrão 'v1'
        :type version: str, optional
        :param extra: Utilizado quando queremos fazer uma busca composta, como albums de um artista, por padrão ""
        :type extra: str, optional
        :return: Resposta do servidor com os dados requisitados.
        :rtype: dict
        """
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}/{extra}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_artist(self, _id):
        """Função que faz o requerimento usando o a função get_resource pegando os dados de um artista pelo ID do artista.

        :param _id: ID do artista na plataforma do Spotify. Facilmente adquirido no link da pagina do artista.
        :type _id: str
        :return: Dicionário com todas as informações do artista.
        :rtype: dict
        """
        return self.get_resource(_id, resource_type="artists")
    
    def get_artist_albums(self, _id):
        """Função que faz o requerimento usando o a função get_resource pegando os albums de um artista pelo ID do artista.

        :param _id: ID do artista na plataforma do Spotify. Facilmente adquirido no link da pagina do artista.
        :type _id: str
        :return: Dicionário com todas as informações acerca dos albuns desse artista.
        :rtype: dict
        """
        return self.get_resource(_id, resource_type="artists", extra="albums")    
    
    def get_album(self, _id):
        """Função que faz o requerimento usando o a função get_resource pegando os dados de um album pelo ID do album.

        :param _id: ID do album na plataforma do Spotify. Facilmente adquirido no link do album ou na pagina do artista.
        :type _id: str
        :return: Dicionário com todas as informações do album.
        :rtype: dict
        """
        return self.get_resource(_id, resource_type="albums")  

    def get_album_track(self, _id):
        """Função que faz o requerimento usando o a função get_resource pegando as musicas de um album pelo ID do album.

        :param _id: ID do album na plataforma do Spotify. Facilmente adquirido no link do album ou na pagina do artista.
        :type _id: str
        :return: Dicionário com todas as informações das musicas do album.
        :rtype: dict
        """
        return self.get_resource(_id, resource_type="albums", extra="tracks")

    def get_track(self, _id):
        """Função que faz o requerimento usando o a função get_resource pegando os dados de uma musica pelo ID da musica.

        :param _id: ID da musica na plataforma do Spotify. Facilmente adquirido no link da musica ou na pagina do album.
        :type _id: str
        :return: Dicionário com todas as informações da musica.
        :rtype: dict
        """
        return self.get_resource(_id, resource_type="tracks")