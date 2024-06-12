import streamlit as st
import openai
import requests
import json
from googletrans import Translator

def translate_text(text, src_language, dest_language):
    translator = Translator()
    translation = translator.translate(text, src=src_language, dest=dest_language)
    return translation.text

def detect_language(text):
    translator = Translator()
    detection = translator.detect(text)
    return detection.lang

def get_prediction(user_input: str) -> int:
    url = "https://buddyapi-qncgwxayla-ew.a.run.app/predict"
    params = {"txt": user_input}
    response = requests.get(url, params=params)
    if response.status_code == 200 and "prediction" in response.json():
        return response.json()["prediction"]
    else:
        return f"An Error {response.status_code} has occurred while retrieving the prediction."

def main():
    st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")

    # Custom styling for the title
    st.markdown(
        """
        <style>
            .title {
                font-size: 52px;
                font-weight: bold;
                color: #87CEEB; /* Sky blue color */
                text-align: left;
                padding-top: 20px;
                padding-bottom: 20px;
                text-shadow: 2px 2px #888888;
            }

            /* Style for chat messages */
            .chat-message {
                padding: 10px;
                margin: 10px;
                border-radius: 10px;
                max-width: 70%;
            }

            /* Style for user messages */
            .user-message {
                background-color: #DCF8C6; /* Light green background */
                align-self: flex-start;
            }

            /* Style for assistant messages */
            .assistant-message {
                background-color: #F0F0F0; /* Light gray background */
                align-self: flex-end;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.title('🤖 Your AI Buddy')

    # Get OpenAI key
    key = st.secrets["openai"]["OpenAI_key"]
    openai.api_key = key

    # Set up the API endpoint and headers
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"  # Replace 'key' with your actual API key
    }

    # Initialize session state
    introduction_line = "Hi! How are you feeling today?"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": introduction_line}]
        st.session_state.exchange_count = 0
        st.session_state.prediction = 0
        st.session_state.open = True

    # Display conversation
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Keep chatbot open until conditions are met
    if st.session_state.open:

        # Text input for manual typing
        user_input = st.chat_input("Talk to your AI Buddy...")
        if user_input:
            user_language = detect_language(user_input)
            st.chat_message("user").markdown(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.exchange_count += 1
            messages = [
                {"role": "system", "content": '''You're a friendly and caring chatbot
                 that's been trained to help people who are feeling depressed or suicidal.
                 Your goal is to provide a safe and supportive space for users to express their feelings and thoughts.
                 You should ask open-ended questions to encourage users to talk, and actively listen to their responses.
                 '''},
                *st.session_state.chat_history
            ]
            data = {
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "max_tokens": 120
            }
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response_data = json.loads(response.text)
            assistant_response = response_data["choices"][0]["message"]["content"]

            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

            # Display assistant answer
            with st.chat_message("assistant"):
                st.markdown(assistant_response)

            # Getting user content for prediction
            user_messages = "".join(item["content"] for item in st.session_state.chat_history if item["role"] == 'user')

            # Translate user messages to English for prediction
            translated_user_messages = translate_text(user_messages, src_language=user_language, dest_language='en')
            st.session_state.prediction = get_prediction(translated_user_messages)

            # If too many sessions or prediction is too high, the chat closes
            if st.session_state.prediction > 0.85:
                st.warning("End of conversation")
                end_prompt = '''You're a friendly and caring chatbot operating in Belgium
                     and you've been trained to help people who are feeling depressed or suicidal.
                     Your goal is to provide a safe and supportive space for users to express their feelings and thoughts.
                     The user you are currently talking with has shown great signs of distress.
                     Can you give him some advice and point him in the right direction?
                     Be caring while giving some good advice.
                     However, the situation is really concerning'''
                end_message = [
                    {"role": "system", "content": end_prompt},
                    *st.session_state.chat_history
                ]
                data = {
                    "model": "gpt-3.5-turbo",
                    "messages": end_message,
                    "max_tokens": 1000
                }
                response = requests.post(url, headers=headers, data=json.dumps(data))
                response_data = json.loads(response.text)
                end_assistant_response = response_data["choices"][0]["message"]["content"]
                with st.chat_message("assistant"):
                    st.markdown(end_assistant_response)
                    st.markdown("In Belgium, you can call 1813, the suicide prevention hotline. They're available 24/7 to listen and help.")
                st.session_state.open = False

            elif st.session_state.prediction > 0.5 and st.session_state.exchange_count > 5:
                st.warning("End of conversation")
                end_prompt = '''You are a friendly, caring chatbot operating in Belgium and have been trained to help people who are feeling depressed or suicidal.
                Your goal is to provide users with a safe and supportive space to express their feelings and thoughts.
                The user you're talking to is showing signs of sadness. However, the situation doesn't seem to be really worrying.
                Can you give him some advice to cheer him up? Be caring while giving some good advice.'''
                end_message = [
                    {"role": "system", "content": end_prompt},
                    *st.session_state.chat_history
                ]
                data = {
                    "model": "gpt-3.5-turbo",
                    "messages": end_message,
                    "max_tokens": 1000
                }
                response = requests.post(url, headers=headers, data=json.dumps(data))
                response_data = json.loads(response.text)
                end_assistant_response = response_data["choices"][0]["message"]["content"]
                with st.chat_message("assistant"):
                    st.markdown(end_assistant_response)
                st.session_state.open = False

            elif st.session_state.exchange_count > 5:
                st.warning("End of conversation")
                with st.chat_message("assistant"):
                    st.markdown("Thank you for this nice discussion! Have a nice day")
                st.session_state.open = False

            else:
                st.session_state.open = True


if __name__ == "__main__":
    main()
