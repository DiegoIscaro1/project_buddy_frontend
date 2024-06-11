import streamlit as st
import openai
import requests
import json

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
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.exchange_count = 0

    # Display conversation
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # First line of conversation
    if st.session_state.exchange_count == 0:
        introduction_line = "Hi! How are you feeling today?"
        st.chat_message("assistant").markdown(introduction_line)

    # Text input for manual typing
    user_input = st.chat_input("Talk to your AI Buddy...")
    if user_input:
        if st.session_state.exchange_count < 4:
            st.chat_message("user").markdown(user_input)
            st.session_state.chat_history.append({"role":"user","content":user_input})
            st.session_state.exchange_count += 1

            messages = [
                    {"role": "system", "content": '''You're a chatbot that's supposed to help people who are depressed or even suicidal.
    The aim is to ask them simple questions to try understand their feelings.
    Try to act as a psychologist.
    Be concise'''},
                    *st.session_state.chat_history
                    ]

            data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": 75
        }
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response_data = json.loads(response.text)
            assistant_response = response_data["choices"][0]["message"]["content"]

            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

            # Display assistant answer
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
        else :
            st.chat_message("user").markdown(user_input)
            st.session_state.chat_history.append({"role":"user","content":user_input})
            st.warning("The conversation has ended. Analyzing the conversation...")

            # Getting user content for prediction
            user_messages = "".join(item["content"] for item in st.session_state.chat_history if item["role"] == 'user')
            prediction = f"Prediction: {get_prediction(user_messages)}"
            st.session_state.chat_history.append({"role": "model", "content": prediction})
            st.chat_message("model").markdown(prediction)

if __name__ == "__main__":
    main()
