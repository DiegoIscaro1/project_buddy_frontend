import streamlit as st
import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Charger le modèle BERT pré-entraîné
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased')

# Définir la fonction pour la détection de risque de suicide
def detect_suicide_risk(text):
    inputs = tokenizer(text, return_tensors='pt')
    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)
    if probs[0, 1] > 0.5:
        return True
    else:
        return False

# Définir la fonction pour générer une réponse
def generate_response(is_suicidal):
    if is_suicidal:
        return "I am sorry you feel that way. You should contact this phone number and seek for help : +324009876"
    else:
        return "I am glad, I wish you an amazing day !"

# Définir la fonction pour envoyer un message à l'API
def send_message(message):
    response = requests.post('http://localhost:5000/api/messages', json={'message': message})
    return response.json()

# Créer l'interface utilisateur Streamlit
st.title('Tell me how you feel today')
st.write('...')

message = st.text_input('What do you want to say?')

if message:
    # Détecter le risque de suicide dans le texte de l'utilisateur
    is_suicidal = detect_suicide_risk(message)

    # Générer une réponse appropriée
    response = generate_response(is_suicidal)

    # Afficher la réponse dans l'interface utilisateur
    st.write(response)

    # Envoyer le message de l'utilisateur et la réponse du chatbot à l'API
    user_message = send_message(message)
    bot_message = send_message(response)
