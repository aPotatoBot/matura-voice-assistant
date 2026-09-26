# pip install vosk
# download https://alphacephei.com/vosk/models -> vosk-model-small-en-us-0.15
import time
current_time = time.time()

import subprocess
import json
from vosk import Model, KaldiRecognizer

spoken_input_list = ["What is the capital of Switzerland?","What is the capital of Switzerland?","What is the capital of Switzerland?",
                     "Write a short story. This short story should be exactly 200 words long.","Write a short story. This short story should be exactly 200 words long.",
                     "Write a short story. This short story should be exactly 200 words long.",
                     "What is the sum of 253 and 12?","What is the sum of 253 and 12?","What is the sum of 253 and 12?",
                     "Create a recipe with a little more sugar to bake a raspberry pie.","Create a recipe with a little more sugar to bake a raspberry pie.",
                     "Create a recipe with a little more sugar to bake a raspberry pie.","Could you please repeat the answer to the first request I made?",
                     "Could you please repeat the answer to the first request I made?","Could you please repeat the answer to the first request I made?"]

model = Model("vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

spoken_prompt = ""
print(time.time() - current_time)
for spoken_input in spoken_input_list:
    input(f"Input: {spoken_input}")
    current_time = time.time()
    audioinput = subprocess.Popen("pw-record --rate=16000 --channels=1 --format=s16 -", shell=True, stdout=subprocess.PIPE)
    
    output = ""
    while not output:
        data = audioinput.stdout.read(8000)
        if rec.AcceptWaveform(data):
            current_rec = rec.Result()
            if json.loads(current_rec)["text"]:
                output = json.loads(current_rec)["text"]
                
    print(f"Output: {output}")
    audioinput.stdout.close()
    audioinput.kill()
    print(f"Time: {time.time() - current_time}")
