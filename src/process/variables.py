"""Common variables"""
from os.path import dirname, join, normpath, abspath

script_dir = dirname(abspath(__file__))


logins_path = normpath(join(script_dir, "..", "resources", "logins.toml"))
ideas_path = normpath(join(script_dir, "..", "resources", "done_ideas.txt"))
story_path = normpath(join(script_dir, "..", "resources", "story.txt"))
mp3_story_path = normpath(join(script_dir, "..", "resources", "story.mp3"))
