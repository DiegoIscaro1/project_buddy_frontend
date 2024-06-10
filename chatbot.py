import streamlit as st
import requests

def get_prediction(user_input):
    url = "https://buddyapi-qncgwxayla-ew.a.run.app/predict"
    params = {"txt": user_input}
    response = requests.get(url, params=params)
    if response.status_code == 200 and "prediction" in response.json():
        return response.json()["prediction"]
    else:
        return "Une erreur s'est produite lors de la récupération de la prédiction."

def chatbot(user_input):
    output = get_prediction(user_input)
    return output

def main():
    st.title("Chatbot")

    user_input = st.text_input("Tapez votre message ici...")

    if st.button("Envoyer"):
        if user_input:
            with st.spinner("Le chatbot réfléchit..."):
                response = chatbot(user_input)
            st.write("Chatbot :", response)

if __name__ == "__main__":
    main()
