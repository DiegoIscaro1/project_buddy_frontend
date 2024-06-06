import streamlit as st
import requests

st.title("Buddy the bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("What is up?")
if prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send a GET request to your API
    response = requests.get("http://localhost:8001/predict", params={"str": prompt})

    # Print the JSON response for debugging
    print(response.json())

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response.json()["prediction"])
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.json()["prediction"]})
