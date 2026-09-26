# Install espeak-ng
import subprocess
import time

current_time = time.time()
input_list = ["Hello, I am ready.","Pi is an irrational number which was calculated by Archimedes around 250 BC to two decimal points, which corresponds to 3.14.","Are you alright? Yes, I'm fine, thanks.","This is the ***best*** raspberry pie recipe! I am 100% certain of that. :)"]

for text_input in input_list:
    subprocess.run(f'espeak-ng "{text_input}"', shell = True)
    print(time.time() - current_time)
    input("Press enter to continue")
    current_time = time.time()
