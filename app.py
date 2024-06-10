import streamlit as st
import requests
import os

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        st.write("Recognizing...")
        try:
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
    return None

def get_prediction(user_input):
    url = "https://buddyapi-qncgwxayla-ew.a.run.app/predict"
    params = {"txt": user_input}
    response = requests.get(url, params=params)
    if response.status_code == 200 and "prediction" in response.json():
        return response.json()["prediction"]
    else:
        return "An error occurred while fetching the prediction."

def chatbot(user_input):
    output = get_prediction(user_input)
    return output

def main():
    st.set_page_config(page_title="Chatbot", page_icon="🤖")

    # Use the correct path format
    image_path = "/home/diego/code/KiruaaSan/project_buddy/Buddy.jpg"

    if os.path.exists(image_path):
        st.sidebar.image(image_path, width=100)
    else:
        st.sidebar.write("Image not found")

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

    st.markdown('<p class="title">Buddy</p>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    def submit():
        user_input = st.session_state.user_input
        if user_input:
            with st.spinner("The chatbot is thinking..."):
                response = chatbot(user_input)
            st.session_state.messages.append(("You", user_input))
            st.session_state.messages.append(("Chatbot", response))
            st.session_state.user_input = ""

    # Text input for manual typing
    st.text_input("Type your message here...", key="user_input", on_change=submit)

    if st.session_state.messages:
        for sender, message in st.session_state.messages:
            if sender == "You":
                st.markdown(f'<div style="text-align: right; margin-bottom: 10px;"><div style="display: inline-block; background-color: #d3e0ff; padding: 10px; border-radius: 10px;">{message}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="text-align: left; margin-bottom: 10px;"><div style="display: inline-block; background-color: #D3D3D3; padding: 10px; border-radius: 10px;">{message}</div></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
