import streamlit as st

# Placeholder function to simulate ML/DL model behavior
def is_problematic(sentence):
    # Dummy implementation: random decision for demo purposes
    # Replace this logic with actual ML/DL model inference
    keywords = ["help", "emergency", "problem", "issue", "urgent"]
    if any(keyword in sentence.lower() for keyword in keywords):
        return True
    return False

# Function to get a response based on the user input
def get_response(user_input):
    if is_problematic(user_input):
        return "This person needs help."
    else:
        return "Thank you for sharing."

# Streamlit app layout
st.title("Do you need help ?")
st.write("Tell me what is going on")

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# User input
user_input = st.text_input("You:", "")

# Handle user input
if user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})
    response = get_response(user_input)
    st.session_state.conversation.append({"role": "assistant", "content": response})
    st.text_input("You:", value="", key=len(st.session_state.conversation))  # Clear the input box after submission

# Display conversation
for message in st.session_state.conversation:
    if message["role"] == "user":
        st.write(f"You: {message['content']}")
    else:
        st.write(f"Chatbot: {message['content']}")
