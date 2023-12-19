from elevenlabs import generate, save
from bing_image_downloader import downloader

# Manually load options
first_option = input("First option: ")
second_option = input("Second option: ")

# Generate the audio
audio = generate(
  text="¿Cuál prefieres?" + first_option + "     o," + second_option,
  voice="Adam",
  model="eleven_multilingual_v2"
)

save(audio, "audio.mp3")

# Get images
downloader.download(first_option, limit=1, output_dir='images', force_replace=False)
downloader.download(second_option, limit=1, output_dir='images', force_replace=False)
