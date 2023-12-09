import sys

from tiktokvoice import tts

from variables import story_path, mp3_story_path

# use TikTok AI voice via this project:
# https://github.com/Giooorgiooo/TikTok-Voice-TTS/tree/main

input_file = open(story_path, "r").read()
sys.getsizeof(input_file)
tts(input_file, "en_us_010", mp3_story_path)
