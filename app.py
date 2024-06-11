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
    key = st.secrets.openai.OpenAI_key
    openai.api_key = key

    # Set up the API endpoint and headers
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.exchange_count = 0
        st.session_state.user_responses = []

    # Define the questions
    questions = [
        "How are you feeling today?",
        "How has your sleep been lately?",
        "How is your social life going?"
    ]

    # Display conversation
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display the current question
    if st.session_state.exchange_count < len(questions):
        current_question = questions[st.session_state.exchange_count]
        st.chat_message("assistant").markdown(current_question)

        # Display predefined options for the current question
        options = ["Perfect!", "Good", "Okay", "Bad", "Really bad"]
        user_choice = st.selectbox("Choose your response:", options, key=st.session_state.exchange_count)

        if st.button("Submit", key=f"submit_{st.session_state.exchange_count}"):
            st.session_state.chat_history.append({"role": "user", "content": user_choice})
            st.session_state.user_responses.append(user_choice)
            st.session_state.exchange_count += 1
            st.experimental_rerun()  # Rerun the script to display the next question or analyze the responses

    # Once all questions are answered, analyze the responses
    if st.session_state.exchange_count == len(questions):
        st.warning("The conversation has ended. Analyzing the responses...")

        # Aggregate the responses
        aggregated_responses = " ".join(st.session_state.user_responses)
        prediction = f"Prediction: {get_prediction(aggregated_responses)}"
        st.session_state.chat_history.append({"role": "model", "content": prediction})
        st.chat_message("model").markdown(prediction)
        st.session_state.exchange_count += 1  # To prevent re-analysis on rerun

if __name__ == "__main__":
    main()
