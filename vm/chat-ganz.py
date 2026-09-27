# curl -fsSL https://ollama.com/install.sh | sh
# ollama pull phi3:mini
import ollama
prompt_list = ["Hello","What is the capital of Switzerland?","What about Germany?","Sweden?",
               "Write a short story. This short story should be exactly 200 words long.",
               "What is the sum of 253 and 12?","Tell me an interesting fact about any country.",
               "Write a short recipe for baking a raspberry pie.",
               "Create a recipe with a little more sugar to bake a raspberry pie.",
               "Could you please repeat the answer to the first request I made?"]
context = [{'role':'system','content':'You give short and decisive answers'}]
total_duration = 0
for current_prompt in prompt_list:
    print("User: ", current_prompt)
    context.append({'role':'user', 'content':current_prompt})
    response = ollama.chat(model='phi3:mini',messages=context)
    print(response['message']['content'])
    context.append({'role':'assistant', 'content':response['message']['content']})
    print('Duration: ', response['total_duration'] / 1000000000)
    total_duration += (response['total_duration'] / 1000000000)
print("Total duration: ", total_duration)
