import streamlit as st
import cohere

# Clave de API de Cohere
API_KEY = st.secrets["cohere"]["api_key"]

# Configuración de la página
st.set_page_config(
    page_title="Chatbot Personalizado",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Fondo oscuro */
    body {
        background-color: #1e1e1e;
        color: #f5f5f5;
    }
    .chat-message {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .user-message {
        background-color: #007bff;
        color: white;
        text-align: right;
    }
    .chatbot-message {
        background-color: #2a2a2a;
        color: white;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💬 Chatbot Personalizado con Cohere y Streamlit")

# Inicializar el estado de los mensajes
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "CHATBOT", "message": "Hola! ¿Cómo puedo asistirte hoy?"}
    ]

# Mostrar historial de mensajes con estilo
for msg in st.session_state.messages:
    role_class = "user-message" if msg["role"] == "USER" else "chatbot-message"
    st.markdown(
        f"<div class='chat-message {role_class}'>{msg['message']}</div>",
        unsafe_allow_html=True
    )

# Entrada del usuario
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Crear campo de entrada de chat
user_input = st.text_input(
    "Escribe tu mensaje aquí...",
    value=st.session_state["user_input"],
    key="input_box",
    placeholder="Escribe algo y presiona Enter..."
)

if st.button("Enviar") or user_input.strip():
    # Guardar el mensaje del usuario
    st.session_state.messages.append({"role": "USER", "message": user_input.strip()})
    
    # Mostrar el mensaje en el chat
    st.markdown(
        f"<div class='chat-message user-message'>{user_input.strip()}</div>",
        unsafe_allow_html=True
    )

    # Crear un prompt con el historial completo
    conversation_history = "\n".join([f"{msg['role']}: {msg['message']}" for msg in st.session_state.messages])
    
    # Generar respuesta del chatbot
    client = cohere.Client(API_KEY)
    response = client.generate(
        model='command-xlarge-nightly',
        prompt=conversation_history,
        max_tokens=200
    )
    chatbot_message = response.generations[0].text.strip()
    
    # Guardar y mostrar el mensaje del chatbot
    st.session_state.messages.append({"role": "CHATBOT", "message": chatbot_message})
    st.markdown(
        f"<div class='chat-message chatbot-message'>{chatbot_message}</div>",
        unsafe_allow_html=True
    )
    
    # Limpiar el campo de entrada
    st.session_state["user_input"] = ""
