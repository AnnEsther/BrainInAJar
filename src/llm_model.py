import ollama
import GLOBALS

def get_response_from_prompt(userPrompt):
    if userPrompt == None:
        return
    try:
        response = ollama.generate(model=GLOBALS.LLM_MODEL, prompt=userPrompt)
    except:
        print("An exception occurred")
    # print(response['response'])
    return response['response']

# getMistralResponse("Tell me something about Joy Mathew")