"""Uses TikTok's API to do Text to Speech processing"""
import sys

from tiktokvoice import tts

from variables import story_path, mp3_story_path

"""
English voice list

English AU - Female	   | en_au_001
English AU - Male	   | en_au_002
English UK - Male 1	   | en_uk_001
English UK - Male 2	   | en_uk_003
English US - Female 1  | en_us_001
English US - Female 2  | en_us_002
English US - Male 1	   | en_us_006
English US - Male 2	   | en_us_007
English US - Male 3	   | en_us_009
English US - Male 4	   | en_us_010
"""

# use TikTok AI voice via this project:
# https://github.com/Giooorgiooo/TikTok-Voice-TTS/tree/main
input_file = open(story_path, "r").read()
tts(input_file, "en_us_010", mp3_story_path)
