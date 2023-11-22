import os
from moviepy.editor import VideoFileClip

INPUT_DIRECTORY = "vidIn/"
VIDEO_OUTPUT_DIRECTORY = "vidOut/"
AUDIO_OUTPUT_DIRECTORY = "audioOut/"

input_videos = os.listdir(INPUT_DIRECTORY)

for video_name in input_videos:
    video = VideoFileClip(INPUT_DIRECTORY + video_name)
    new_clip = video.without_audio()
    audio = video.audio
    if audio != None:
        new_clip.write_videofile(VIDEO_OUTPUT_DIRECTORY + video_name)
        audio.write_audiofile(AUDIO_OUTPUT_DIRECTORY + video_name[:-3] + ".wav")
    else:
        print(video_name + " has failed because it is missing the audio.")
