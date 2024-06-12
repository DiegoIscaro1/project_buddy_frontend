import streamlit as st
import openai
import requests
import json
import translate
import langdetect

def translate_text(text, src_language='auto', dest_language='en'):
    if src_language != 'en':
        translator = translate.Translator(from_lang=src_language, to_lang=dest_language)
        translation = translator.translate(text)
        return translation
    else:
        return text

def get_prediction(user_input: str) -> float:
    url = "https://buddyapi-qncgwxayla-ew.a.run.app/predict"
    params = {"txt": user_input}
    response = requests.get(url, params=params)
    if response.status_code == 200 and "prediction" in response.json():
        return response.json()["prediction"]
    else:
        return 0.0

def main():
    st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")

    st.title('🤖 Your AI Buddy')
    st.markdown('🚨 This chatbot offers support for emotional distress but is not a substitute for professional help or emergency services. In a crisis, please call emergency services🚨')

    openai.api_key = st.secrets["openai"]["OpenAI_key"]

    # Add CSS for the restart button
    st.markdown(
        """
        <style>
            .restart-button {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background-color: #f63366;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                z-index: 1000;
            }
            .restart-button:hover {
                background-color: #d12f5b;
            }
        </style>
        <script>
            function restartChatbot() {
                document.getElementById('restart-button').click();
            }
        </script>
        """, unsafe_allow_html=True
    )

    # Create the restart button
    if st.button("Restart Chatbot", key="restart"):
        st.session_state.clear()
        st.experimental_rerun()

    introduction_line = "Hi! How are you feeling today?"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": introduction_line}]
        st.session_state.exchange_count = 0
        st.session_state.open = True

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.open:
        user_input = st.chat_input("Talk to your AI Buddy...")
        if user_input:
            st.chat_message("user").markdown(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.exchange_count += 1

            user_language = langdetect.detect(user_input)

            translated_user_input = translate_text(user_input, src_language=user_language)
            st.session_state.prediction = get_prediction(translated_user_input)
            #st.markdown(st.session_state.prediction) # To check probability

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
                "max_tokens": 150
            }
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai.api_key}"
            }
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response_data = json.loads(response.text)
            assistant_response = response_data["choices"][0]["message"]["content"]

            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

            with st.chat_message("assistant"):
                st.markdown(assistant_response)

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

            elif st.session_state.prediction > 0.5:
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
