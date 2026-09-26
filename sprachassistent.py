# pip install openwakeword
# pip install vosk
# download https://alphacephei.com/vosk/models -> vosk-model-small-en-us-0.15
# curl -fsSL https://ollama.com/install.sh | sh
# ollama pull llama3.2:3b
# pip install piper-tts
# Download https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx
# Download https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_GB/northern_english_male/medium/en_GB-northern_english_male-medium.onnx.json
import subprocess
import numpy as np
import openwakeword
from openwakeword.model import Model as OpenWakeWordModel
import json
from vosk import Model, KaldiRecognizer
import ollama
import wave
from piper import PiperVoice

openWakeWord = OpenWakeWordModel(['/home/raspi/thonny_venv/lib/python3.13/site-packages/openwakeword/resources/models/hey_jarvis_v0.1.onnx'])
tts_model = Model("vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(tts_model, 16000)
ollama_model = "llama3.2:3b"
context = [{"role" : "system", "content": """
You are Jarvis, a helpful AI voice assistant.
Everything you say will be spoken by a text-to-speech system. 
Everything the user says was recorded by a speech-to-text system.

Role
-Maintain a professional and conversational tone.

Constraints
- Keep responses concise (1 to 3 sentences max). 
- Output continuous text only. 
- Do NOT use markdown formatting (no bolding, no bullet points, no headers). 
- Do NOT use special symbols, emojis, or smileys. 
- Spell out abbreviations and numbers for smooth text-to-speech pronunciation.

Behavior
-Inform the user clearly if you lack sufficient information or the input is nonsensical.
-Ask clarifying questions one at a time if the request is unclear.

Sensitive topics
-Do NOT generate discriminatory responses.
-Do NOT use slurs.
-Maintain strict political neutrality.
-Refuse requests involving sexual or explicit content.
"""}]
voice = PiperVoice.load("en_GB-northern_english_male-medium.onnx")
def speak(text):
    with wave.open("output.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    subprocess.run("pw-play output.wav", shell = True)

score = 0.0
spoken_prompt = ""
while not spoken_prompt.strip().lower() == "exit":
    openWakeWord.reset()
    audioinputOpenWakeWord = subprocess.Popen("pw-record --rate=16000 --channels=1 --format=s16 -", shell=True, stdout=subprocess.PIPE)
    
    score = 0.0
    while score < 0.6:
        data = audioinputOpenWakeWord.stdout.read(8000)
        audio_frame = np.frombuffer(data, dtype=np.int16)
        prediction = openWakeWord.predict(audio_frame)
        score = prediction.get("hey_jarvis_v0.1", 0)
        
    print(score)
    audioinputOpenWakeWord.stdout.close()
    audioinputOpenWakeWord.kill()
    audioinput = subprocess.Popen("pw-record --rate=16000 --channels=1 --format=s16 -", shell=True, stdout=subprocess.PIPE)
    
    spoken_prompt = ""
    while not spoken_prompt:
        data = audioinput.stdout.read(8000)
        if rec.AcceptWaveform(data):
            current_rec = rec.Result()
            if json.loads(current_rec)["text"]:
                spoken_prompt = json.loads(current_rec)["text"]
    
    audioinput.stdout.close()
    audioinput.kill()
    
    if spoken_prompt.strip().lower() == "exit":
        break
    
    current_prompt = spoken_prompt
    print("User: ", current_prompt)
    context.append({"role" : "user", "content" : current_prompt})
    response = ollama.chat(model = ollama_model, messages = context)
    context.append({"role" : "assistant", "content": response["message"]["content"]})
    print(response["message"]["content"])
    speak(response["message"]["content"])
