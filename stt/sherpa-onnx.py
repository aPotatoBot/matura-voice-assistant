# download tokens.txt from https://huggingface.co/bookbot/sherpa-onnx-ort-streaming-zipformer-en-2023-06-26/tree/main
# download encoder-epoch-99-avg-1-chunk-16-left-128.int8.ort from https://huggingface.co/bookbot/sherpa-onnx-ort-streaming-zipformer-en-2023-06-26/tree/main
# download decoder-epoch-99-avg-1-chunk-16-left-128.int8.ort from https://huggingface.co/bookbot/sherpa-onnx-ort-streaming-zipformer-en-2023-06-26/tree/main
# download joiner-epoch-99-avg-1-chunk-16-left-128.int8.ort from https://huggingface.co/bookbot/sherpa-onnx-ort-streaming-zipformer-en-2023-06-26/tree/main
# pip install sherpa-onnx
import time
current_time = time.time()

import subprocess
import numpy as np
import sherpa_onnx as sherpa

spoken_input_list = ["What is the capital of Switzerland?","What is the capital of Switzerland?","What is the capital of Switzerland?","Write a short story. This short story should be exactly 200 words long.","Write a short story. This short story should be exactly 200 words long.","Write a short story. This short story should be exactly 200 words long.","What is the sum of 253 and 12?","What is the sum of 253 and 12?","What is the sum of 253 and 12?","Create a recipe with a little more sugar to bake a raspberry pie.","Create a recipe with a little more sugar to bake a raspberry pie.","Create a recipe with a little more sugar to bake a raspberry pie.","Could you please repeat the answer to the first request I made?","Could you please repeat the answer to the first request I made?","Could you please repeat the answer to the first request I made?"]
sample_rate = 48000
samples_per_read = int(0.1*sample_rate)
bytes_per_read = samples_per_read * 4

recognizer =  sherpa.OnlineRecognizer.from_transducer(
    tokens="/home/raspi/Tests/sherpa-onnx/tokens.txt",
    encoder="/home/raspi/Tests/sherpa-onnx/encoder-epoch-99-avg-1-chunk-16-left-128.int8.ort",
    decoder="/home/raspi/Tests/sherpa-onnx/decoder-epoch-99-avg-1-chunk-16-left-128.int8.ort",
    joiner="/home/raspi/Tests/sherpa-onnx/joiner-epoch-99-avg-1-chunk-16-left-128.int8.ort",
    num_threads=1,
    sample_rate=16000,
    feature_dim=80,
    enable_endpoint_detection=True,
    rule1_min_trailing_silence=2.4,
    rule2_min_trailing_silence=1.2,
    rule3_min_utterance_length=300,
    )
stream = recognizer.create_stream()

spoken_prompt = ""
print(time.time() - current_time)
for spoken_input in spoken_input_list:
    input(f"Input: {spoken_input}")
    current_time = time.time()
    audioinput = subprocess.Popen("pw-record --raw --rate=48000 --channels=1 --format=f32 -", shell=True, stdout=subprocess.PIPE)
    
    output = ""
    while not output:
        samples = audioinput.stdout.read(bytes_per_read)
        array_samples = np.frombuffer(samples, dtype = np.float32)
        stream.accept_waveform(sample_rate, array_samples)
        while recognizer.is_ready(stream):
            recognizer.decode_stream(stream)
        result = recognizer.get_result(stream)
        if recognizer.is_endpoint(stream):
            output = result
            recognizer.reset(stream)

    print(f"Output: {output}")
    audioinput.stdout.close()
    audioinput.kill()
    print(f"Time: {time.time() - current_time}")
