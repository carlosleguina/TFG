import streamlit as st
import spacy
from typing import List, Dict
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.llms.openai import OpenAI

# Cargando el modelo NLP de Spacy para español
nlp = spacy.load("es_core_news_sm")

# Definiciones de categorías y plantillas de preguntas
CATEGORIAS = ['general', 'aspecto', 'olor', 'textura', 'sabor', 'color', 'dureza', 'dulzura']
PLANTILLAS_PREGUNTAS = {
    'general': "¿Puedes contarme más en general?",
    'aspecto': "¿Cómo describirías su aspecto?",
    'olor': "¿Qué me puedes decir sobre su olor?",
    'textura': "¿Cómo describirías su textura?",
    'sabor': "¿Qué me puedes decir sobre su sabor?",
    'color': "¿Cómo describirías su color?",
    'dureza': "¿Qué tan duro es?",
    'dulzura': "¿Puedes comentar sobre su nivel de dulzura?",
}

def analizar_respuesta(respuesta: str) -> Dict[str, List[str]]:
    doc = nlp(respuesta)
    contenido_categorizado = {categoria: [] for categoria in CATEGORIAS}
    
    # Lógica de categorización real basada en el análisis de la respuesta
    for token in doc:
        # Esta es una simplificación; se debería mejorar la lógica de mapeo
        if token.pos_ == "NOUN":
            contenido_categorizado['general'].append(token.text)
    
    return contenido_categorizado

def identificar_campos_faltantes(contenido_categorizado: Dict[str, List[str]]) -> List[str]:
    campos_faltantes = [campo for campo, contenido in contenido_categorizado.items() if not contenido]
    return campos_faltantes

def generar_preguntas(campos_faltantes: List[str]) -> List[str]:
    preguntas = [PLANTILLAS_PREGUNTAS[campo] for campo in campos_faltantes]
    return preguntas

# Inicialización de la interfaz de Streamlit y la lógica del chatbot
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¿Qué te ha parecido la galleta?"}
    ]

if prompt := st.chat_input("Tu respuesta"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    contenido_categorizado = analizar_respuesta(prompt)
    campos_faltantes = identificar_campos_faltantes(contenido_categorizado)
    preguntas_adicionales = generar_preguntas(campos_faltantes)
    
    for pregunta in preguntas_adicionales:
        st.session_state.messages.append({"role": "assistant", "content": pregunta})

    # Suponiendo que ya tienes configurado el servicio y el chat_engine adecuadamente
    # Esta parte se ejecutaría cuando ya no hayan campos faltantes o después de recoger las respuestas adicionales
    # response = chat_engine.chat(prompt)
    # st.session_state.messages.append({"role": "assistant", "content": response.response})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
