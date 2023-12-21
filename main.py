from random import randint
from elevenlabs import voices, generate, save
from bing_image_downloader import downloader
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_audioclips
import os
import PIL
from moviepy.video.VideoClip import TextClip

voices = voices()
random_voice = randint(0, len(voices)-1)

# Manually load options
option1 = input("Primera opción: ")
option2 = input("Segunda opción: ")

# Generate the audio
voice = generate(
  text="¿Cuál prefieres? " + option1 + (" u, " if option2.startswith('o') else " o, ") + option2,
  voice=voices[random_voice],
  model="eleven_multilingual_v2"
)

save(voice, "voice.mp3")

# Get images
downloader.download(option1, limit=2, output_dir="images", adult_filter_off=False, force_replace=False)
downloader.download(option2, limit=2, output_dir="images", adult_filter_off=False, force_replace=False)

# Add audio to video
clips = []
voice = AudioFileClip("voice.mp3")
clock = AudioFileClip("clock.mp3")
template = VideoFileClip("template.mp4").subclip(0, voice.duration + 6)
clips.append(template)

# Add images to video
image1_path = os.listdir("images/" + option1)
image1 = ImageClip("images/" + option1 + "/" + image1_path[0]).set_start(0).set_duration(voice.duration + 6)
image1 = image1.resize((600, 600), PIL.Image.LANCZOS)
image1 = image1.set_pos("top")
clips.append(image1)

image2_path = os.listdir("images/" + option2)
image2 = ImageClip("images/" + option2 + "/" + image2_path[0]).set_start(0).set_duration(voice.duration + 6)
image2 = image2.resize((600, 600), PIL.Image.LANCZOS)
image2 = image2.set_pos("bottom")
clips.append(image2)

# Add text to video
text1 = TextClip(option1, fontsize=70, color="white", font="Arial", size=(1050, None), method="caption")
text1 = text1.set_position(("center", 0.32), relative=True).set_duration(voice.duration + 5.5)
clips.append(text1)

text2 = TextClip(option2, fontsize=70, color="white", font="Arial", size=(1050, None), method="caption")
text2 = text2.set_position(("center", 0.55), relative=True).set_duration(voice.duration + 5.5)
clips.append(text2)

# Render video
audio = concatenate_audioclips([voice, clock])
video = CompositeVideoClip(clips)
result_video = video.set_audio(audio)

result_video.write_videofile("video.mp4", codec="libx264", audio_codec="aac")
