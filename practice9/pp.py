import pygame
import os
def get_playlist():
    all_files=os.listdir('.')
    playlist=[]
    for f in all_files:
        if f.endswith('.mp3') or f.endswith('.wav'):
            playlist.append(f)
    playlist.sort()
    return playlist
def play_song(song_name):
    pygame.mixer.music.load(song_name)
    pygame.mixer.music.play()