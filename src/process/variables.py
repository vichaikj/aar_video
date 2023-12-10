"""Common variables"""
from os.path import dirname, join, normpath, abspath

script_dir = dirname(abspath(__file__))
print(script_dir)


logins_path = normpath(join(script_dir, "..", "resources", "logins.toml"))
ideas_path = normpath(join(script_dir, "..", "resources", "done_ideas.txt"))
story_path = normpath(join(script_dir, "..", "resources", "story.txt"))
mp3_story_path = normpath(join(script_dir, "..", "resources", "story.mp3"))
wav_story_path = normpath(join(script_dir, "..", "resources", "story.wav"))
minecraft_video_path = normpath(join(script_dir, "..", "resources", "videos", "minecraft.mp4"))
video_audio_path = normpath(join(script_dir, "..", "resources", "story.mp4"))
