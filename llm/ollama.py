# curl -fsSL https://ollama.com/install.sh | sh
# ollama pull [MODELL]
import ollama

model = "llama3.2:1b"
promptlist = ["Hello", "What is the capital of Switzerland?", "What about Germany?", "Sweden?", "Write a short story. This short story should be exactly 200 words long.", "What is the sum of 253 and 12?", "Tell me an interesting fact about any country.", "Write a short recipe for baking a raspberry pie.", "Create a recipe with a little more sugar to bake a raspberry pie.", "Could you please repeat the answer to the first request I made?"]
durationlist = [0,0,0,0,0,0,0,0,0,0,]
total_duration = 0

for test in range(3):
    
    context = [{"role" : "system", "content": "You give short and decisive answers."}]
    
    for index in range(len(promptlist)):
        current_prompt = promptlist[index]
        print("User: ", current_prompt)
        context.append({"role" : "user", "content" : current_prompt})
        response = ollama.chat(model = model, messages = context)
        context.append({"role" : "assistant", "content": response["message"]["content"]})
        print(response["message"]["content"])
        print("Duration: ", response["total_duration"] / 1000000000)
        durationlist[index] += response["total_duration"] / 1000000000
        total_duration += response["total_duration"] / 1000000000   
print(durationlist)
print(total_duration)
print(context)
