# git clone https://github.com/neuphonic/neutts-air.git
# pip install -e .
# download espeak-ng
# pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu --force-reinstall
# pip install --upgrade torchtune
# pip install torchao==0.14.1
import subprocess
import soundfile as sf
import torch
import time

current_time = time.time()
input_list = ["Hello, I am ready.","Pi is an irrational number which was calculated by Archimedes around 250 BC to two decimal points, which corresponds to 3.14.","Are you alright? Yes, I'm fine, thanks.","This is the ***best*** raspberry pie recipe! I am 100% certain of that. :)"]
torch.backends.mkldnn.enabled = False
torch.set_default_dtype(torch.float32)

from neuttsair.neutts import NeuTTSAir
tts = NeuTTSAir(backbone_repo="neuphonic/neutts-air", backbone_device="cpu", codec_repo="neuphonic/neucodec", codec_device="cpu")
ref_text = "/home/raspi/neutts-air/samples/dave.txt"
ref_audio_path = "/home/raspi/neutts-air/samples/dave.wav"
ref_text = open(ref_text, "r").read().strip()
ref_codes = tts.encode_reference(ref_audio_path)

def speak(text):
    wav = tts.infer(text, ref_codes, ref_text)
    sf.write("/home/raspi/Tests/output.wav", wav, 24000)
    subprocess.run(f"pw-play /home/raspi/Tests/output.wav", shell = True)

for text_input in input_list:
    speak(text_input)
    print(time.time() - current_time)
    input("Press enter to continue")
    current_time = time.time()
