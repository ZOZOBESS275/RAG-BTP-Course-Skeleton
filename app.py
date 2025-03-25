import streamlit as st
import requests

def generate_response(conversation):
    """
    Sends the conversation history to your local Ollama endpoint and returns the assistant's reply.
    Adjust the payload and endpoint according to your Ollama configuration.
    """
    # Adjust the endpoint and model name as required by your Ollama setup
    endpoint = "http://localhost:11434/v1/chat/completions"
    payload = {
        "model": "your-model-name",  # e.g., "llama2", "gpt4all", etc.
        "messages": conversation,
        "temperature": 0.7
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(endpoint, json=payload, headers=headers)
    if response.status_code == 200:
        # Adjust the extraction based on your Ollama response structure.
        # Here, we assume a response similar to OpenAI's:
        return response.json()["choices"][0]["message"]["content"]
    else:
        st.error(f"Request failed with status {response.status_code}: {response.text}")
        return "Sorry, something went wrong."

# Initialize session state for the conversation if it doesn't exist
if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

st.title("Chat with Ollama (Local LLM)")

# Input for the user's message
user_input = st.text_input("Your message:")

if st.button("Send") and user_input:
    # Append the user's message to the conversation history
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    # Generate a response from the local Ollama instance
    #assistant_response = generate_response(st.session_state.conversation)
    assistant_response = """Les avantages de l'utilisation d'une pompe à chaleur avec un plancher chauffant sont :

1. Chauffage thermodynamique basse température : Cette technologie permet un chauffage efficace et respectueux de l'environnement, en utilisant les énergies renouvelables pour chauffer le plancher.
2. Suppression du bouclage ECS (Équilibreur de Charge Solaire) : En utilisant une pompe à chaleur avec un plancher chauffant, il n'est pas nécessaire d'installer un système de bouclage ECS, ce qui réduit les coûts et l'importance des déchets thermiques.
3. Économie d'énergie : Le chauffage basse température peut réduire la consommation d'énergie pour chauffer le plancher, ce qui peut entraîner une réduction des factures de gaz ou d'électricité.
4. Sécurité et confort : L'utilisation d'une pompe à chaleur avec un plancher chauffant peut améliorer la sécurité et le confort dans les bâtiments, en particulier pour les personnes âgées ou handicapées.
5. Double ou triple service : Cette technologie permet de fournir plusieurs services (chauffage, éclairage et climatisation) à partir d'un même système, ce qui peut réduire la complexité du système et améliorer l'efficacité énergétique.

Il est important de noter que ces avantages sont étayés par les informations fournies dans le fichier "La Pompe à chaleur, des solutions disponibles en habitat collectif.md"."""
    st.session_state.conversation.append({"role": "assistant", "content": assistant_response})

# Display the conversation history
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Assistant:** {msg['content']}")
