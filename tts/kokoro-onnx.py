# download https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0 -> kokoro-v1.0.onnx
# download https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0 -> voices-v1.0.bin
# pip install kokoro-onnx
import time
import soundfile as sf
import subprocess

current_time = time.time()
input_list = ["Hello, I am ready.","Pi is an irrational number which was calculated by Archimedes around 250 BC to two decimal points, which corresponds to 3.14.","Are you alright? Yes, I'm fine, thanks.","This is the ***best*** raspberry pie recipe! I am 100% certain of that. :)"]
from kokoro_onnx import Kokoro
kokoro = Kokoro("/home/raspi/Tests/kokoro-v1.0.onnx", "/home/raspi/Tests/voices/voices-v1.0.bin")
voice = "am_michael"

def speak(text):
    samples, sample_rate = kokoro.create(text, voice = voice, speed = 1.0)
    sf.write("output.wav", samples, sample_rate)
    subprocess.run("pw-play /home/raspi/Tests/output.wav", shell = True)

for text_input in input_list:
    speak(text_input)
    print(time.time() - current_time)
    input("Press enter to continue")
    current_time = time.time()
