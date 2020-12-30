import sys
import requests
import tkinter as tk
from io import BytesIO
from auth import *
from tkinter.font import Font
from PIL import Image, ImageTk

class gui():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("750x500")
        self.root.title("LyricalDisplay")
        self.data = ApiData('--rzqdJGFcVjzUa4sLjvL3ADoT9Bj9bvWFWQCiTut7m41yIH8QVdBetvyDnGWe3n')

        launch_font = Font(family = "Futura", size = 24)
        self.head_font = Font(family = "Futura", size = 18)
        self.body_font = Font(family = "Futura", size = 12)

        #Creates launch page
        self.welcome_label = tk.Label(self.root, text = "Welcome to your Lyrical Display",font = launch_font)
        self.welcome_label.place(relx=0.5, rely=0.4, anchor = 'center')
        self.launch_button = tk.Button(self.root, text = "Show Lyrics", command = self.open_lyrics, font = launch_font, fg = 'blue')
        self.launch_button.place(relx=0.5, rely=0.5, anchor = 'center')

    #Retrieves track name, artist, and lyrics and diplays them on screen
    def open_lyrics(self):
        self.welcome_label.destroy() #Removes launch page and deletes widgets from it
        self.welcome_label = None

        self.launch_button.destroy()
        self.launch_button = None
        self.data.update_song()
        try:
            response = requests.get(self.data.track_image_url) #Retrieves image from URL, processes it and saves it in a variable
            render = Image.open(BytesIO(response.content))
            self.track_image = ImageTk.PhotoImage(render)
        except:
            self.track_image = None

        self.left_frame = tk.Frame(self.root) #Frame to hold track name, artists and refresh button
        self.left_frame.grid(row = 0, column = 0,padx = 10)

        self.right_frame = tk.Frame(self.root)  #Frame to hold lyrics text box
        self.right_frame.grid(row = 0, column = 2,padx = 10)

        if(self.track_image is None):
            self.track_image_display = tk.Label(self.left_frame)
        else:
            self.track_image_display = tk.Label(self.left_frame, image = self.track_image,relief = 'groove')
            self.track_image_display.image = self.track_image
        self.track_image_display.pack()

        if(self.data.track_name is None or self.data.track_artist is None): #If no song is not playing
            self.track_label = tk.Message(self.left_frame, text = "No song currently playing.",font = self.head_font)
        else:
            self.track_label = tk.Message(self.left_frame, text = "Currently playing: '" + self.data.track_name + "' by "+ self.data.track_artist, font = self.head_font)
        self.track_label.pack()

        self.refresh_button = tk.Button(self.left_frame,text = "Refresh", command = self.update_gui)
        self.refresh_button.pack()

        if(self.data.track_lyrics is None):
            self.lyrics_box = tk.Text(self.right_frame, height = 30, width = 50, font = self.body_font)
            self.lyrics_box.config(state = 'disabled')
        else:
            self.lyrics_box = tk.Text(self.right_frame, height = 30, width = 50, font = self.body_font, bg ='#fffed4',relief = 'ridge')
            self.lyrics_box.insert(tk.END,self.data.track_lyrics)
            self.lyrics_box.config(state = 'disabled')
        self.lyrics_box.pack()

    #Updates GUI with new information whenever the currently playing track on Spotify changes.
    def update_gui(self):
        self.data.update_song()
        if(self.data.track_image_url is not None):
            response = requests.get(self.data.track_image_url)
            render = Image.open(BytesIO(response.content))
            self.track_image = ImageTk.PhotoImage(render)

        self.lyrics_box.config(state = 'normal')
        if(self.data.track_name is None or self.data.track_artist is None):
            self.track_label.config(text = "No song currently playing.")
            self.lyrics_box.delete(1.0,tk.END)
            self.lyrics_box.insert(tk.END,"") #Inserts blankspace at the end of the lyrics text box
            self.lyrics_box.config(state = 'disabled')

        else:
            self.track_label.config(text = "Currently playing: '" + self.data.track_name + "' by "+ self.data.track_artist)
            self.lyrics_box.delete(1.0,tk.END)
            self.lyrics_box.insert(tk.END,self.data.track_lyrics) #Inserts new lyrics at the end of the lyrics text box
            self.lyrics_box.config(state = 'disabled', bg ='#fffed4',relief = 'ridge')

            self.track_image_display.config(image = self.track_image,relief = 'groove')
            self.track_image_display.image = self.track_image

    def run_loop(self):
        self.root.mainloop()
