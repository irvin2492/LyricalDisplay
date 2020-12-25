import sys
import tkinter as tk
from tkinter.font import Font
from lyricsgenius import Genius
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --rzqdJGFcVjzUa4sLjvL3ADoT9Bj9bvWFWQCiTut7m41yIH8QVdBetvyDnGWe3n

class ApiData():
    def __init__(self,genius_auth):
        self.__genius_token = genius_auth
        self.gen = Genius(self.__genius_token)
        self.__spotify_ID = "77000a15d6134f888344df26f3880982"
        self.__spotify_secret = "ade88a234dc248c3bcaad91fe63e765b"
        self.user = "spotify:user:irv.in"
        self.sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = self.__spotify_ID,
                                client_secret = self.__spotify_secret,
                                redirect_uri = "https://www.google.com" ,
                                scope = "user-read-currently-playing",
                                username = self.user))

        #Collects track data from Spotify API and uses that to get lyrics from Genius API

        self.__current_track_data = self.sp.current_user_playing_track()
        try:
            self.__current_track_name = self.__current_track_data["item"]["name"]
            self.__current_track_artist = self.__current_track_data["item"]["artists"][0]["name"]
            self.__current_track_duration = self.__current_track_data["item"]["duration_ms"]

            __current_track_lyricdata= self.gen.search_song(self.__current_track_name,self.__current_track_artist)
            self.__current_track_lyrics = __current_track_lyricdata.lyrics
        except:
            self.__current_track_name = None
            self.__current_track_artist = None
            __current_track_lyricdata = None
            self.__current_track_lyrics = None
            self.__current_track_duration = None
            print("No song playing.")

    def update_song(self):
        self.__current_track_data = self.sp.current_user_playing_track()
        try:
            self.__current_track_name = self.__current_track_data["item"]["name"]
            self.__current_track_artist = self.__current_track_data["item"]["artists"][0]["name"]
            self.__current_track_duration = self.__current_track_data["item"]["duration_ms"]

            __current_track_lyricdata= self.gen.search_song(self.__current_track_name,self.__current_track_artist)
            self.__current_track_lyrics = __current_track_lyricdata.lyrics

        except:
            self.__current_track_name = None
            self.__current_track_artist = None
            __current_track_lyricdata = None
            self.__current_track_lyrics = None
            print("No song playing.")

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
    def track_duration(self):
        return self.__current_track_duration

class gui():

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x500")
        self.root.title("LyricalDisplay")
        self.test = ApiData('--rzqdJGFcVjzUa4sLjvL3ADoT9Bj9bvWFWQCiTut7m41yIH8QVdBetvyDnGWe3n')

        headFont = Font(family = "Helvetica", size = 18)
        bodyFont = Font(family = "Helvetica", size = 12)

        if(self.test.track_name is None or self.test.track_artist is None):
            self.track_label = tk.Label(self.root, text = "No song currently playing.")
        else:
            self.track_label = tk.Label(self.root, text = "Currently playing: '" + self.test.track_name + "' by "+ self.test.track_artist, font = headFont)
        self.track_label.pack()

        self.refresh_button = tk.Button(self.root,text = "refresh?", command = self.update_gui)
        self.refresh_button.pack() #testing

        if(self.test.track_lyrics is None):
            self.lyrics_box = tk.Text(self.root, height = 50, width = 50, font = bodyFont)
            self.lyrics_box.config(state = 'disabled')
            self.lyrics_box.pack()

        else:
            self.lyrics_box = tk.Text(self.root, height = 50, width = 50, font = bodyFont)
            self.lyrics_box.insert(tk.END,self.test.track_lyrics)
            self.lyrics_box.config(state = 'disabled')

            self.lyrics_box.pack()

    def update_gui(self):
        self.test.update_song()
        self.lyrics_box.config(state = 'normal')
        if(self.test.track_name is None or self.test.track_artist is None):
            self.track_label.config(text = "No song currently playing.")
            self.lyrics_box.delete(1.0,tk.END)
            self.lyrics_box.insert(tk.END,"")
            self.lyrics_box.config(state = 'disabled')
        else:
            self.track_label.config(text = "Currently playing: '" + self.test.track_name + "' by "+ self.test.track_artist)
            self.lyrics_box.delete(1.0,tk.END)
            self.lyrics_box.insert(tk.END,self.test.track_lyrics)
            self.lyrics_box.config(state = 'disabled')

    def run_loop(self):
        self.root.mainloop()

def main():
    window = gui()
    window.run_loop()

main()
