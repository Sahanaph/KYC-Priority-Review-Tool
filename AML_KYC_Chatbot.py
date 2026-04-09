import requests
from config import API_KEY


def chat_loop():
    messages = [{"role": "system", "content": "You are a KYC and AML banking expert assistant. Answer questions clearly and concisely in simple language.",}]
  
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break
        else:
            messages.append({"role": "user", "content": question})

            body = {"model": "llama-3.3-70b-versatile", "messages": messages}
            
            try:
             response = requests.post(url, headers=headers, json=body)
             data = response.json()
             #print("Raw response:", data)  -- to get the raw response from API to know what's the cause of error
             answer = data["choices"][0]["message"]["content"]
             messages.append({"role": "assistant", "content": answer})

             print("AI:", answer)

            except KeyError:
                print("Error: Unexpected reponse from API. Please try again")
                continue
            except requests.exceptions.ConnectionError:
                print("Error: Could not connect to the API. please check your internet connection and try again")
                continue
            except Exception as e:
                print("Something went wrong", e)
                continue
            
chat = chat_loop()
