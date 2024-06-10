import streamlit as st
import requests
import openai
import json

def get_prediction(user_input: str) -> int:
    url = "https://buddyapi-qncgwxayla-ew.a.run.app/predict"
    params = {"txt": user_input}
    response = requests.get(url, params=params)
    if response.status_code == 200 and "prediction" in response.json():
        return response.json()["prediction"]
    else:
        return f"An Error {response.status_code} has occurred while retrieving the prediction."


def get_answer_chatgpt (messages: list, user_input: str) -> str:

    # Get the openAI key
    key = st.secrets["openai"]["OpenAI_key"]
    openai.api_key = key

    # Add the new user message to the list
    messages.append({"role": "user", "content": user_input})

    # Set up the API endpoint and headers
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"  # Replace 'key' with your actual API key
    }

    # Include all the previous messages in the request data
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 70
    }

    # Make the request and parse the response
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = json.loads(response.text)

    # Get the generated text and add it to the list of messages
    generated_text = response_data["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": generated_text})

    # Return the generated text
    return generated_text


if __name__ == "__main__":
    message_list = []
    preprompt = '''You’re a chatbot that’s supposed to help people who are depressed or even suicidal.
The aim is to ask them simple questions to try and understand their feelings.
The conversation must end after 5 exchanges. Be as attentive as possible, and keep your exchanges as concise as possible.
All conversations will be analyzed by a predictive model to determine whether the person is at risk of suicide.
All you have to do is talk to the user and compile this information into an input to be sent to the model.
Try to not be to instrusive or too specific.
Let’s simulate this chatbot'''
    introduction = get_answer_chatgpt(message_list, preprompt)
    print(f"Assistant : {introduction}")
    for i in range (5):
        print(f"\nUser: ")
        prompt = input()
        answer = get_answer_chatgpt(message_list, prompt)
        print(f"Assistant : {answer}")

    # Getting user content
    user_messages = "".join(item['content'] for item in message_list if item['role'] == 'user')

    prediction = get_prediction(user_messages)
    print(prediction)
