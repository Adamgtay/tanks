import os
from pygame import mixer

def main_music_load(main_sound,duration):
    mixer.music.load(main_sound)
    mixer.music.play(duration)