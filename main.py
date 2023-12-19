from random import randint
from elevenlabs import voices, generate, save
from bing_image_downloader import downloader

voices = voices()
random_voice = randint(0, len(voices)-1)

# Manually load options
first_option = input("First option: ")
second_option = input("Second option: ")

# Generate the audio
audio = generate(
  text="¿Cuál prefieres?" + first_option + "     o," + second_option,
  voice=voices[random_voice],
  model="eleven_multilingual_v2"
)

save(audio, "audio.mp3")

# Get images
downloader.download(first_option, limit=1, output_dir='images', adult_filter_off=False, force_replace=False)
downloader.download(second_option, limit=1, output_dir='images', adult_filter_off=False, force_replace=False)
