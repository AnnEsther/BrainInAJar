import ollama
import GLOBALS

def is_ollama_active():
    response = ollama.pull(model=GLOBALS.LLM_MODEL, stream=True)
    for val in response:
        if val['status'] == 'success':
            print("Ollama active.")
            return
    print("ERROR : Ollama not active")


def is_mistral_active():
    response = ollama.list()
    for model in response["models"]:
        if(model['name'] == "mistral:latest"):
            print("Mistral actice.")
            return
        #print(f"Model : {model['name']:18s}, Parameters : {model['details']['parameter_size']}")
    print("ERROR : Mistral not active")

# checkOllama()
# listOllamaModels()