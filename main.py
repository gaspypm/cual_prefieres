import os
import csv
import spacy
import PIL
from random import randint
from elevenlabs import voices, generate, save
from bing_image_downloader import downloader
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, TextClip, concatenate_audioclips

spacy.prefer_gpu()
voices = voices()
font = "Arial-Rounded-MT-Bold"

# Load options
with open('test_questions.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)
    for index, row in enumerate(reader, start=1):
        option1, option2 = row

        print("Generating", option1 + (" u, " if option2.startswith('o') else " o, ") + option2 + "...")

        # Generate the audio
        random_voice = randint(0, len(voices)-1)

        voice = generate(
          text="¿Cuál prefieres? " + option1 + (" u, " if option2.startswith('o') else " o, ") + option2,
          voice=voices[random_voice],
          model="eleven_multilingual_v2"
        )

        save(voice, "voice.mp3")

        # Get images
        nlp = spacy.load("es_core_news_sm")
        doc1 = nlp(option1)
        doc2 = nlp(option2)

        simplified_option1 = " ".join(token.text for token in doc1 if token.pos_ in ["NOUN", "VERB"])
        simplified_option2 = " ".join(token.text for token in doc2 if token.pos_ in ["NOUN", "VERB"])

        downloader.download(simplified_option1, limit=2, output_dir="images", adult_filter_off=False, force_replace=False)
        downloader.download(simplified_option2, limit=2, output_dir="images", adult_filter_off=False, force_replace=False)

        # Add audio to video
        clips = []
        voice = AudioFileClip("voice.mp3")
        clock = AudioFileClip("clock.mp3")
        template = VideoFileClip("template.mp4").subclip(0, voice.duration + 8)
        clips.append(template)

        # Add images to video
        image1_path = os.listdir("images/" + simplified_option1)
        image1 = ImageClip("images/" + simplified_option1 + "/" + image1_path[0]).set_start(0).set_duration(voice.duration + 8)
        image1 = image1.resize((600, 600), PIL.Image.LANCZOS)
        image1 = image1.set_pos("top")
        clips.append(image1)

        image2_path = os.listdir("images/" + simplified_option2)
        image2 = ImageClip("images/" + simplified_option2 + "/" + image2_path[0]).set_start(0).set_duration(voice.duration + 8)
        image2 = image2.resize((600, 600), PIL.Image.LANCZOS)
        image2 = image2.set_pos("bottom")
        clips.append(image2)

        # Add text to video
        text1 = TextClip(option1, fontsize=70, color="white", font=font, size=(1050, None), method="caption")
        text1 = text1.set_position(("center", 0.32), relative=True).set_duration(voice.duration + 6.5)
        clips.append(text1)

        text2 = TextClip(option2, fontsize=70, color="white", font=font, size=(1050, None), method="caption")
        text2 = text2.set_position(("center", 0.55), relative=True).set_duration(voice.duration + 6.5)
        clips.append(text2)

        # Add results
        percentage = randint(25, 50)
        print(percentage)
        print(100-percentage)
        result1 = TextClip(str(percentage) + "%",
                           fontsize=100,
                           color=("green" if percentage >= 50 else "red"),
                           font=font,
                           stroke_color='white',
                           stroke_width=4)
        result1 = result1.set_position(("center", 0.35), relative=True).set_duration(1.5).set_start(voice.duration + 6.5)
        clips.append(result1)

        result2 = TextClip(str(100-percentage) + "%",
                           fontsize=100,
                           color=("green" if percentage <= 50 else "red"),
                           font=font,
                           stroke_color='white',
                           stroke_width=4)
        result2 = result2.set_position(("center", 0.60), relative=True).set_duration(1.5).set_start(voice.duration + 6.5)
        clips.append(result2)

        # Render video
        audio = concatenate_audioclips([voice, clock])
        video = CompositeVideoClip(clips)
        result_video = video.set_audio(audio)

        output_file = f"videos/video_{index}.mp4"
        result_video.write_videofile(output_file, codec="libx264", audio_codec="aac")



