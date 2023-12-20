from random import randint
from elevenlabs import voices, generate, save
from bing_image_downloader import downloader
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip

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
voice_duration = voice.duration
template = VideoFileClip("template.mp4").subclip(0, voice_duration + 6)
clips.append(template)
