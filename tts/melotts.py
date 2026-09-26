# git clone https://github.com/myshell-ai/MeloTTS.git
# sudo apt update
# sudo apt install mecab libmecab-dev mecab-ipadic-utf8 -y
# pip install upgrade pip
# pip install tokenizers --prefer-binary
# cd MeloTTS
# pip install --no-deps -e .
# pip install transformers librosa scipy num2words cached_path
# pip install anyascii eng-to-ipa g2p_en inflect loguru txtsplit unidecode
# pip install cn2an pypinyin mecab-python3
# pip install jieba jamo langid g2pkk
# pip install pypinyin
# sudo mkdir -p /usr/local/etc 
# sudo ln -s /etc/mecabrc /usr/local/etc/mecabrc
# pip install fugaschi
# pip install unidic_lite
# pip install gruut
# python -c "import nltk; nltk.download('averaged_perceptron_tagger_eng')"
import subprocess
import time

current_time = time.time()
input_list = ["Hello, I am ready.","Pi is an irrational number which was calculated by Archimedes around 250 BC to two decimal points, which corresponds to 3.14.","Are you alright? Yes, I'm fine, thanks.","This is the ***best*** raspberry pie recipe! I am 100% certain of that. :)"]
from melo.api import TTS
speed = 1.0
output_path = "/home/raspi/Tests/output.wav"
device = "cpu"
model = TTS(language = "EN", device = device)
speaker_ids = model.hps.data.spk2id

def speak(text):
    model.tts_to_file(text, speaker_ids["EN-Default"], output_path, speed = speed)
    subprocess.run("pw-play /home/raspi/Tests/output.wav", shell = True)   

for text_input in input_list:
    speak(text_input)
    print(time.time() - current_time)
    input("Press enter to continue")
    current_time = time.time()
