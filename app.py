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
    st.warning('''
⚠️ This chatbot offers support for emotional distress but is not a substitute for professional help or emergency services. In a crisis, please call emergency services! ⚠️
''')

    # Setting up openai chat
    openai.api_key = st.secrets["openai"]["OpenAI_key"]
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    # Include the provided CSS
    custom_css = '''
    <style>
    /* Style the chat messages */
    .stMarkdown {
        font-size: 20px;
    }
    </style>
    '''

    # Embed the CSS in the Streamlit app
    st.markdown(custom_css, unsafe_allow_html=True)

    # Initiate the chatbot
    introduction_line = "Hi! How are you feeling today?"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": introduction_line}]
        st.session_state.exchange_count = 0
        st.session_state.open = True

    # Display chat_history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            message_content = message["content"]
            st.markdown(f'<p class="stMarkdown">{message_content}</p>', unsafe_allow_html=True)


    # Input cell for user
    if st.session_state.open:
        user_input = st.chat_input("Talk to your AI Buddy...")

        if user_input:
            st.chat_message("user").markdown(f'<p class="stMarkdown">{user_input}</p>', unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.exchange_count += 1

            # Translation
            user_language = langdetect.detect(user_input)
            translated_user_input = translate_text(user_input, src_language=user_language)

            # Prediction analysis
            with st.spinner('Analysing discussion...'):
                st.session_state.prediction = get_prediction(translated_user_input)
            # st.markdown(st.session_state.prediction) # To check probability

                # If prediction high -> ask chatbot to redirect user through right people
                if st.session_state.prediction > 0.85:

                    end_prompt = '''You are a friendly, caring chatbot operating in Belgium
                        and you've been trained to help people who are feeling depressed or suicidal.
                        The user you are talking to is showing great signs of distress.
                        Give him a comforting reply for him to feel better. Don't ask a question.
                        '''
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
                        st.markdown(f'<p class="stMarkdown">{end_assistant_response}</p>', unsafe_allow_html=True)

                    st.info('''Community Help Service (CHS): A 24/7 helpline available in English for anyone in need.
                            They can be reached at 02 648 40 14 or through their website at www.chsbelgium.org.''', icon="ℹ️")
                    st.session_state.open = False
                    st.button('Restart Chat', on_click=st.session_state.clear)

                # If prediction high but not too concerning -> ask chatbot to give some advice
                elif st.session_state.prediction > 0.35 and st.session_state.exchange_count > 5:

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
                        st.markdown(f'<p class="stMarkdown">{end_assistant_response}</p>', unsafe_allow_html=True)
                    st.session_state.open = False
                    st.info('Need Well-Being advice in Belgium? 🇧🇪 Visit [Psychosocial Support](https://centredecrise.be/fr/que-pouvez-vous-faire/ensemble/soutien-international/soutien-pyschosocial-en-belgique/je-cherche)', icon="ℹ️")
                    st.button('Restart Chat', on_click=st.session_state.clear)

                # If prediction low -> keep talking with user
                else:
                    messages = [
                    {"role": "system", "content": '''You're a friendly and caring chatbot
                    that's been trained to help people who are feeling depressed or suicidal.
                    Your goal is to provide a safe and supportive space for users to express their feelings and thoughts.
                    You should ask open-ended questions to encourage users to talk, and actively listen to their responses.
                    Try to remain neutral in your question. Don't exceed 100 tokens in your answer!
                    '''},
                    *st.session_state.chat_history
                ]
                    data = {
                        "model": "gpt-3.5-turbo",
                        "messages": messages,
                        "max_tokens": 100
                    }

                    response = requests.post(url, headers=headers, data=json.dumps(data))
                    response_data = json.loads(response.text)
                    assistant_response = response_data["choices"][0]["message"]["content"]

                    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

                    with st.chat_message("assistant"):
                        st.markdown(f'<p class="stMarkdown">{assistant_response}</p>', unsafe_allow_html=True)
                    st.session_state.open = True

if __name__ == "__main__":
    main()
