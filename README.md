# LyricalDisplay
Python program that creates a GUI to diplay song lyrics. for use with my account to automatically display lyrics from Genius based on the song that I'm listening to.

## How it works
The program connects to my Spotify account using the 'spotipy' module. Once connected, it
retrieves the relevant information from the track and sends the track name and artist to the
Genius API. Using the 'LyricsGenius' module, it retrieves the lyrics. Finally, all
the track information and song lyrics are used along with the 'tkinter' module
to create a GUI for me to view.
