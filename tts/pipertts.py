# install piper-tts
# download https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx
# download https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx.json
import time
import wave
import subprocess

current_time = time.time()
input_list = ["Hello, I am ready.","Pi is an irrational number which was calculated by Archimedes around 250 BC to two decimal points, which corresponds to 3.14.","Are you alright? Yes, I'm fine, thanks.","This is the ***best*** raspberry pie recipe! I am 100% certain of that. :)"]
from piper import PiperVoice
voice = PiperVoice.load("/home/raspi/Tests/voices/en_GB-northern_english_male-medium.onnx")

def speak(text):
    with wave.open("output.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    subprocess.run("pw-play /home/raspi/Tests/output.wav", shell = True)

for text_input in input_list:
    speak(text_input)
    print(time.time() - current_time)
    input("Press enter to continue")
    current_time = time.time()
