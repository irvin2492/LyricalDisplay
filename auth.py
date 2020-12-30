import spotipy
from lyricsgenius import Genius
from spotipy.oauth2 import SpotifyOAuth

# --rzqdJGFcVjzUa4sLjvL3ADoT9Bj9bvWFWQCiTut7m41yIH8QVdBetvyDnGWe3n "Genius authorization code got from website"

class ApiData():
    def __init__(self,genius_auth):
        self.__genius_token = genius_auth
        self.gen = Genius(self.__genius_token)
        self.__spotify_ID = "77000a15d6134f888344df26f3880982" # Generated from Spotify Api
        self.__spotify_secret = "ade88a234dc248c3bcaad91fe63e765b" # Generated from Spotify Api
        self.user = "spotify:user:irv.in"
        self.sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = self.__spotify_ID,
                                client_secret = self.__spotify_secret,
                                redirect_uri = "https://www.google.com" ,
                                scope = "user-read-currently-playing",
                                username = self.user))

        #Collects track data from Spotify API
        self.__current_track_data = self.sp.current_user_playing_track()

    #Using track data from Spotify Api, this function takes information from it and gets lyrics from Genius Api
    def get_lyrics(self):
        try:
            self.__current_track_name = self.__current_track_data["item"]["name"]
            self.__current_track_artist = self.__current_track_data["item"]["artists"][0]["name"]
            self.__current_track_image_url = self.__current_track_data["item"]["album"]["images"][1]["url"] #medium size image
            self.__current_track_is_local = self.__current_track_data["item"]["is_local"]

            __current_track_lyricdata= self.gen.search_song(self.__current_track_name,self.__current_track_artist)
            self.__current_track_lyrics = __current_track_lyricdata.lyrics

        except:
            self.__current_track_name = None
            self.__current_track_artist = None
            __current_track_lyricdata = None
            self.__current_track_lyrics = None
            self.__current_track_image_url = None
            self.__current_track_is_local = None

    #Retrieves new track information from Spotify API
    def update_song(self):
        self.__current_track_data = self.sp.current_user_playing_track()
        try:
            self.__current_track_name = self.__current_track_data["item"]["name"]
            self.__current_track_artist = self.__current_track_data["item"]["artists"][0]["name"]
            self.__current_track_image_url = self.__current_track_data["item"]["album"]["images"][1]["url"] #medium size image
            self.__current_track_is_local = self.__current_track_data["item"]["is_local"]

            __current_track_lyricdata= self.gen.search_song(self.__current_track_name,self.__current_track_artist)
            self.__current_track_lyrics = __current_track_lyricdata.lyrics

        except:
            self.__current_track_name = None
            self.__current_track_artist = None
            self.__current_track_image_url = None
            self.__current_track_is_local = None
            __current_track_lyricdata = None
            self.__current_track_lyrics = None

    @property #testing only
    def track_data(self):
        return self.__current_track_data

    @property
    def track_name(self):
        return self.__current_track_name
    @property
    def track_artist(self):
        return self.__current_track_artist
    @property
    def track_lyrics(self):
        return self.__current_track_lyrics
    @property
    def track_image_url(self):
        return self.__current_track_image_url
    @property
    def track_locality(self):
        return self.__current_track_is_local
