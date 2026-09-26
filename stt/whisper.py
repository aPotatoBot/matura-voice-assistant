# pip install whisper
# pip install -U openai-whisper
import time
current_time = time.time()

import subprocess
import whisper

rectime = 5
spoken_input_list = ["What is the capital of Switzerland?","What is the capital of Switzerland?","What is the capital of Switzerland?","Write a short story. This short story should be exactly 200 words long.","Write a short story. This short story should be exactly 200 words long.","Write a short story. This short story should be exactly 200 words long.","What is the sum of 253 and 12?","What is the sum of 253 and 12?","What is the sum of 253 and 12?","Create a recipe with a little more sugar to bake a raspberry pie.","Create a recipe with a little more sugar to bake a raspberry pie.","Create a recipe with a little more sugar to bake a raspberry pie.","Could you please repeat the answer to the first request I made?","Could you please repeat the answer to the first request I made?","Could you please repeat the answer to the first request I made?"]

model = whisper.load_model("tiny.en")

spoken_prompt = ""
print(time.time() - current_time)
for spoken_input in spoken_input_list:
    input(f"Input: {spoken_input}")
    current_time = time.time()
    audioinput = subprocess.run(f"timeout {rectime} pw-record --rate=16000 --channels=1 --format=s16 /home/raspi/Tests/input.wav", shell=True)
    output = model.transcribe("/home/raspi/Tests/input.wav")["text"]
    print(f"Output: {output}")
    print(f"Time: {time.time() - current_time}")
