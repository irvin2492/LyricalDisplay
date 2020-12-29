import sys
import spotipy
import requests
import tkinter as tk
from io import BytesIO
from tkinter.font import Font
from PIL import Image, ImageTk
from lyricsgenius import Genius
from spotipy.oauth2 import SpotifyOAuth

# --rzqdJGFcVjzUa4sLjvL3ADoT9Bj9bvWFWQCiTut7m41yIH8QVdBetvyDnGWe3n "Spotify authorization code"

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
            print("No song playing.")

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
    def track_image_url(self):
        return self.__current_track_image_url
    @property
    def track_locality(self):
        return self.__current_track_is_local

class gui():

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("700x700")
        self.root.title("LyricalDisplay")
        self.test = ApiData('--rzqdJGFcVjzUa4sLjvL3ADoT9Bj9bvWFWQCiTut7m41yIH8QVdBetvyDnGWe3n')

        launch_font = Font(family = "Futura", size = 24)
        self.head_font = Font(family = "Futura", size = 18)
        self.body_font = Font(family = "Futura", size = 12)

        self.launch_label = tk.Button(self.root, text = "Show Lyrics", command = self.open_lyrics, font = launch_font)
        self.launch_label.pack()

    #Retrieves track name, artist, and lyrics and diplays them on screen
    def open_lyrics(self):
        self.launch_label.destroy()
        self.launch_label = None
        self.test.update_song()
        try:
            response = requests.get(self.test.track_image_url) #Retrieves image from URL, processes it and saves it in a variable
            render = Image.open(BytesIO(response.content))
            self.track_image = ImageTk.PhotoImage(render)
        except:
            self.track_image = None

        self.left_frame = tk.Frame(self.root) #Frame to hold track name, artists and refresh button
        self.left_frame.grid(row = 0, column = 0)

        self.right_frame = tk.Frame(self.root)  #Frame to hold lyrics text box
        self.right_frame.grid(row = 0, column = 1)

        if(self.track_image is None):
            self.track_image_display = tk.Label(self.left_frame)
        else:
            self.track_image_display = tk.Label(self.left_frame, image = self.track_image)
            self.track_image_display.image = self.track_image
        self.track_image_display.pack()

        if(self.test.track_name is None or self.test.track_artist is None):
            self.track_label = tk.Label(self.left_frame, text = "No song currently playing.")
        else:
            self.track_label = tk.Label(self.left_frame, text = "Currently playing: '" + self.test.track_name + "' by "+ self.test.track_artist, font = self.head_font)
        self.track_label.pack()

        self.refresh_button = tk.Button(self.left_frame,text = "Refresh", command = self.update_gui)
        self.refresh_button.pack()

        if(self.test.track_lyrics is None):
            self.lyrics_box = tk.Text(self.right_frame, height = 50, width = 50, font = self.body_font)
            self.lyrics_box.config(state = 'disabled')
        else:
            self.lyrics_box = tk.Text(self.right_frame, height = 50, width = 50, font = self.body_font, background = "beige")
            self.lyrics_box.insert(tk.END,self.test.track_lyrics)
            self.lyrics_box.config(state = 'disabled')
        self.lyrics_box.pack()## TODO:     MAKE LYRICS STICK TO RIGHT

    #Updates GUI with new information whenever the currently playing track on Spotify changes.
    def update_gui(self):
        self.test.update_song()
        if(self.test.track_image_url is not None):
            response = requests.get(self.test.track_image_url)
            render = Image.open(BytesIO(response.content))
            self.track_image = ImageTk.PhotoImage(render)

        self.lyrics_box.config(state = 'normal')
        if(self.test.track_name is None or self.test.track_artist is None):
            self.track_label.config(text = "No song currently playing.")
            self.lyrics_box.delete(1.0,tk.END)
            self.lyrics_box.insert(tk.END,"") #Inserts blankspace at the end of the lyrics text box
            self.lyrics_box.config(state = 'disabled')

        else:
            self.track_label.config(text = "Currently playing: '" + self.test.track_name + "' by "+ self.test.track_artist)
            self.lyrics_box.delete(1.0,tk.END)
            self.lyrics_box.insert(tk.END,self.test.track_lyrics) #Inserts new lyrics at the end of the lyrics text box
            self.lyrics_box.config(state = 'disabled')
            self.track_image_display.config(image = self.track_image)
            self.track_image_display.image = self.track_image

    def run_loop(self):
        self.root.mainloop()

def main():
    window = gui()
    window.run_loop()

main()
