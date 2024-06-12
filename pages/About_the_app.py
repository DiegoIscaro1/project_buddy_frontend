import streamlit as st
from PIL import Image

# Function to display image with custom text
def display_image_with_text(image_path, text):
    image = Image.open(image_path)
    st.image(image, caption=text, use_column_width=True)

def main():
    st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")

    st.sidebar.markdown("""
    <style>
    .css-18e3th9 {
        font-size: 24px;
        font-weight: 600;
        color: #FFD700; /* Gold color */
        text-align: left;
        padding-top: 30px;
        padding-bottom: 30px;
        text-shadow: 2px 2px #888888;
        border-left: 6px solid #FFD700;
        padding-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


    st.title('🤖 Your AI Buddy')

    # Add navigation menu
    page = ("About the app")

    if page == "About the app":
        chat_page()

def chat_page():
    # Chat page content

    st.write("## Welcome to Your AI Buddy! 🤖")

    st.write("Your AI Buddy is an innovative chatbot designed to provide emotional support and assistance to users. Leveraging advanced artificial intelligence, Your AI Buddy engages in thoughtful conversations to understand your feelings and provide helpful responses. Whether you're feeling down, need someone to talk to, or simply want to share your thoughts, Your AI Buddy is here for you.")

    st.write("### Key Features:")

    st.write("- **Empathetic Conversations**: Your AI Buddy is trained to respond with empathy and understanding, acting like a virtual psychologist to help you navigate your emotions.")
    st.write("- **Smart Analysis**: Using cutting-edge AI technology, Your AI Buddy can analyze the tone and content of your messages to offer appropriate responses and support.")
    st.write("- **Safe Space**: Your AI Buddy offers a confidential and non-judgmental environment where you can freely express your thoughts and feelings.")


    st.write("### Why Use Your AI Buddy?")

    st.write("- **Emotional Support**: When you're feeling overwhelmed, anxious, or depressed, Your AI Buddy is here to listen and provide comfort.")
    st.write("- **Accessibility**: Available anytime, anywhere, Your AI Buddy offers instant support without the need for appointments or waiting times.")
    st.write("- **Personalized Interactions**: Your AI Buddy tailors its responses to your unique situation, ensuring you receive the care and attention you need.")

    st.write("Your AI Buddy is more than just a chatbot; it's a compassionate companion designed to help you through tough times. Start a conversation today and discover the support and understanding that Your AI Buddy can offer.")

if __name__ == "__main__":
    main()
