import streamlit as st
import requests
import configparser
from llama.querry_maker import expand_query

def query_ollama(prompt, model="llama3.2"):
    prompt = expand_query(prompt)
    config = configparser.ConfigParser()
    config.read("config.ini")

    server = config["llama"]["server"]
    response = requests.post(
        server,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False  # you can use True if you want streamed responses
        }
    )
    data = response.json()
    return data["response"]

# For demonstration, we'll simulate a local LLM response.
# Replace this function with your actual LLM call (e.g., to Ollama).
def generate_response(conversation):
    pass

# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "text": "You are a helpful assistant."}
    ]

st.title("Chat with LLM")

# Option 1: Use streamlit-chat library if installed
try:
    from streamlit_chat import message as chat_message
    chat_lib_available = True
except ImportError:
    chat_lib_available = False

# Input for the user's message
user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "text": user_input})
    # Generate and append assistant's response

    #response = generate_response(st.session_state.messages[-1]['text'])
    response = query_ollama(st.session_state.messages[-1]['text'])
    st.session_state.messages.append({"role": "assistant", "text": response})

# Display the conversation
st.markdown("## Conversation:")

if chat_lib_available:
    # Display each message with a chat bubble style, assigning unique keys
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            chat_message(msg["text"], is_user=True, key=f"user_{idx}")
        elif msg["role"] == "assistant":
            chat_message(msg["text"], is_user=False, key=f"assistant_{idx}")
else:
    # Fallback display using basic markdown formatting
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['text']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Assistant:** {msg['text']}")
            
