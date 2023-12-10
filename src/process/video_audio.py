from moviepy.config import change_settings
from moviepy.editor import VideoFileClip, AudioFileClip
from random import randint

from variables import minecraft_video_path, mp3_story_path, video_audio_path

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})


def overlay_audio_on_video(video_path, audio_path, output_path):
    # Load video and audio clips
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Get the duration of the video and audio clips
    video_duration = video_clip.duration
    audio_duration = audio_clip.duration

    # Generate a random start time for overlay
    start_time = randint(1, int(video_duration - audio_duration)-1)

    # Extract the subclip from the video to overlay the audio
    video_subclip = video_clip.subclip(round(start_time-0.5, 2), round(start_time+audio_duration+0.5, 2))

    # Set the audio of the subclip to the loaded audio clip
    video_subclip = video_subclip.set_audio(audio_clip)

    # Write the final video with overlaid audio
    video_subclip.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)


overlay_audio_on_video(minecraft_video_path, mp3_story_path, video_audio_path)


