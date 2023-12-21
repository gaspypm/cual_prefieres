from random import randint
from elevenlabs import voices, generate, save
from bing_image_downloader import downloader
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_audioclips
import os
import PIL

voices = voices()
random_voice = randint(0, len(voices)-1)

# Manually load options
first_option = input("Primera opción: ").lower()
second_option = input("Segunda opción: ").lower()

# Generate the audio
voice = generate(
  text="¿Cuál prefieres?" + first_option + "                           o," + second_option,
  voice=voices[random_voice],
  model="eleven_multilingual_v2"
)

save(voice, "voice.mp3")

# Get images
downloader.download(first_option, limit=2, output_dir='images', adult_filter_off=False, force_replace=False)
downloader.download(second_option, limit=2, output_dir='images', adult_filter_off=False, force_replace=False)

# Add audio to video
clips = []
voice = AudioFileClip("voice.mp3")
clock = AudioFileClip("clock.mp3")
template = VideoFileClip("template.mp4").subclip(0, voice.duration + 6)
clips.append(template)

# Add images to video
image1_path = os.listdir("images/" + first_option)
image1 = ImageClip("images/" + first_option + "/" + image1_path[0]).set_start(0).set_duration(voice.duration + 6)
image1 = image1.resize((600, 600), PIL.Image.LANCZOS)
image1 = image1.set_pos("top")
clips.append(image1)

image2_path = os.listdir("images/" + second_option)
image2 = ImageClip("images/" + second_option + "/" + image2_path[0]).set_start(0).set_duration(voice.duration + 6)
image2 = image2.resize((600, 600), PIL.Image.LANCZOS)
image2 = image2.set_pos("bottom")
clips.append(image2)

audio = concatenate_audioclips([voice, clock])
video = CompositeVideoClip(clips)
result_video = video.set_audio(audio)

result_video.write_videofile("video.mp4", codec="libx264", audio_codec="aac")
