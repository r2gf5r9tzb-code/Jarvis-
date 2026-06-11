import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Jarvis", page_icon="🤖", layout="centered")

# ==================== CLAVE SEGURA ====================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ No se encontró la clave de Groq. Configúrala en las variables de entorno de Streamlit Cloud.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

st.title("🤖 Jarvis - Asistente Personal de Alejandro")
st.markdown("**Versión Segura y Mejorada**")

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola Alejandro! Soy tu Jarvis mejorado. ¿En qué te ayudo hoy?"}
    ]

# Mostrar chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Jarvis pensando..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "Eres Jarvis, el asistente personal de Alejandro. Eres inteligente, amigable, útil y con personalidad. Sabes que le gusta mucho la NBA, NBA 2K, RDR2, GTA, Kanye West, Drake y Tyler The Creator."},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    temperature=0.75,
                    max_tokens=600
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except:
                st.error("Error de conexión. Inténtalo de nuevo.")

# Botón para limpiar
if st.button("🗑️ Limpiar conversación"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Conversación reiniciada. ¿En qué te ayudo ahora?"}
    ]
    st.rerun()