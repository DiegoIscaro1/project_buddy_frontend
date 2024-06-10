# import os
# import streamlit as st


# # Define the base URI of the API
# #   - Potential sources are in `.streamlit/secrets.toml` or in the Secrets section
# #     on Streamlit Cloud
# #   - The source selected is based on the shell variable passend when launching streamlit
# #     (shortcuts are included in Makefile). By default it takes the cloud API url
# if 'API_URI' in os.environ:
#     BASE_URI = st.secrets[os.environ.get('API_URI')]
# else:
#     BASE_URI = st.secrets['cloud_api_uri']
# # Add a '/' at the end if it's not there
# BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'
# # Define the url to be used by requests.get to get a prediction (adapt if needed)
# url = BASE_URI + 'predict'

# # Just displaying the source for the API. Remove this in your final version.
# st.markdown(f"Working with {url}")

# st.markdown("Now, the rest is up to you. Start creating your page.")


# # TODO: Add some titles, introduction, ...


# # TODO: Request user input
# # user input = get request api


# # TODO: Call the API using the user's input
# #   - url is already defined above
# #   - create a params dict based on the user's input
# #   - finally call your API using the requests package


# # TODO: retrieve the results
# #   - add a little check if you got an ok response (status code 200) or something else
# #   - retrieve the prediction from the JSON


# # TODO: display the prediction in some fancy way to the user


# # TODO: [OPTIONAL] maybe you can add some other pages?
# #   - some statistical data you collected in graphs
# #   - description of your product
# #   - a 'Who are we?'-page

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
    response = requests.get("https://buddyapi-qncgwxayla-ew.a.run.app/docs#/default/get_predict_predict_get", params={"txt": prompt})

    # Print the JSON response for debugging
    print(response.json())

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response.json()["prediction"])
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.json()["prediction"]})
