import requests
import datetime
from urllib.parse import urlencode
import base64

class SpotifyAPI(object):
    """Class that defines the spotify object. Agregates all methods to make the requests to spotify API.

    :param object: The base class of the class hierarchy.
    :type object: object
    :raises Exception: Exception raised when there are no client id and secret.
    :return: Spotify object that have all the methods bellow.
    :rtype: object
    """
    
    access_token = None 
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, *args, **kwargs):
        """Init method. Sets the client id and secret to the web app created on spotify api server.
        """
        super().__init__(*args, **kwargs)
        self.client_id = "28afa3960a524b87943dc0426a022a3e"
        self.client_secret = "6fbdae782c3440c28835590d9146b00f"
    
    def get_client_credentials(self):
        """Method that returns the credential enconded in Base64.

        :raises Exception: Raised when there is no client id and server.
        :return: returns the credential enconded in Base64
        :rtype: base64
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        """Function that gets the token header based on the credentials generated.

        :return: The token header.
        :rtype: dict
        """

        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def perform_auth(self):
        """Method the performs the authentication of the device on Spotify API.

        :raises Exception: Raised id the response is out of the specified range.
        :return: Informas if the authentication was successfull. 
        :rtype: boolean
        """

        token_url = self.token_url
        token_data = {
            "grant_type": "client_credentials"
        } 
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        """Function that generates the acess token. 

        :return: Token to acess the API.
        :rtype: str
        """
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token

    def get_resource_header(self):
        """Generates the header used in the endpoint when calling the API.

        :return: Header with the acess token.
        :rtype: dict
        """
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
        
    def get_resource(self, lookup_id, resource_type, version='v1', extra=""):
        """Method that looks the specified endpoint in the API.

        :param lookup_id: ID that is being requestm represents the type of information is being requested.
        :type lookup_id: str
        :param resource_type: Type of information that is being requested.
        :type resource_type: str
        :param version: API version, by default 'v1'
        :type version: str, optional
        :param extra: Used for extended searchs, by default ""
        :type extra: str, optional
        :return: API response.
        :rtype: dict
        """
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}/{extra}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_artist(self, _id):
        """Method that uses the get_resource method to request the artist by its id.

        :param _id: Artist ID on Spotify. 
        :type _id: str
        :return: Dictionary with artist's information.
        :rtype: dict
        """
        return self.get_resource(_id, resource_type="artists")
    
    def get_artist_albums(self, _id):
        """Method that uses the get_resource method to request the artist's albums by its id.

        :param _id: Artist ID on Spotify.
        :type _id: str
        :return: Dictionary with artist's album information.
        :rtype: dict
        """
        return self.get_resource(_id, resource_type="artists", extra="albums")    
    
    def get_album(self, _id):
        """Method that uses the get_resource method to request the album by its id.

        :param _id: Album ID on Spotify.
        :type _id: str
        :return: Dictionary with album's information.
        :rtype: dict
        """
        return self.get_resource(_id, resource_type="albums")  

    def get_album_track(self, _id):
        """Method that uses the get_resource method to request the album's tracks by its id.

        :param _id: Album ID on Spotify.
        :type _id: str
        :return: Dictionary with album's track information.
        :rtype: dict
        """
        return self.get_resource(_id, resource_type="albums", extra="tracks")

    def get_track(self, _id):
        """Method that uses the get_resource method to request the track by its id.

        :param _id: Track ID on Spotify.
        :type _id: str
        :return: Dictionary with tracks's information.
        :rtype: dict
        """
        return self.get_resource(_id, resource_type="tracks")