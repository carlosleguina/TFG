import streamlit as st

from back import Bot
from back import embedding


def main():

    if 'bot' not in st.session_state:
        st.session_state['bot'] = Bot()

    chatbot = st.session_state['bot']
    st.set_page_config(
        page_title= "IncluSens",
        page_icon = "Images/ddc1f5c9342dc000a0ae23a42bb6fb47.png"
    )

    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image('Images/0cc28c3adebdd5716286e2b298089aa8.png',width = 250)

    if 'end' not in st.session_state.keys():
        st.session_state['end'] = False

    placeholder = st.empty()  # Crear un placeholder para el contenido futuro

    if st.session_state['end']:
            st.write("<h1 style='text-align: center;'>¡Muchas gracias por rellenar el Formulario!</h1>", unsafe_allow_html=True) 
    else:

        st.markdown("<h1 style='text-align: center;'>IncluSens: Cookie Chatbot</h1>", unsafe_allow_html=True)
        st.markdown("""
        <p style='text-align: justify; font-size: 20px;margin-bottom: 0px;'>Prueba la galleta y danos tu opinión sobre ella de la manera más detallada posible. Puedes probar la galleta tanto como necesites. Si necesitas más galletas pídelas al responsable de cata.</p>
        <p style='text-align: justify; font-size: 20px;margin-bottom: 0px;'>Te recordamos que es importante que escribas todo lo que pienses sobre la galleta:</p>
        <p style='text-align: justify; font-size: 20px;margin-bottom: 0px; margin-left: 40px;'>- Si te gusta o no</p>
        <p style='text-align: justify; font-size: 20px;margin-bottom: 0px; margin-left: 40px;'>- Lo que te gusta de la galleta</p>
        <p style='text-align: justify; font-size: 20px;margin-bottom: 0px; margin-left: 40px;'>- Lo que no te gusta de la galleta</p>
        <p style='text-align: justify; font-size: 20px;margin-bottom: 0px; margin-left: 40px;'>- Que te parecen sus características sensoriales como la textura, el aspecto, el sabor, el olor, ...</p>
        <p style='text-align: justify; font-size: 20px;margin-bottom: 0px;'>Si has probado otras galletas antes, no compares esta galleta con las anteriores. Habla solo de las características de esta galleta</p>
        """, unsafe_allow_html=True)

        if "messages" not in st.session_state.keys(): # Initialize the chat message history
            st.session_state['messages'] = True
            chatbot.reset_conversation_history()

        if st.session_state['end'] == False:
            if prompt := st.chat_input("Tu respuesta"): # Prompt for user input and save to chat history
                chatbot.add_conversation(role="user", content=prompt)
                if 'consumer_code' not in st.session_state.keys():
                    st.session_state['consumer_code'] = prompt
                    chatbot.set_consumer_code(prompt)
                elif 'consumer_code' in st.session_state.keys() and 'cookie_code' not in st.session_state.keys():
                    st.session_state['cookie_code'] = prompt
                    chatbot.set_cookie_code(prompt)
                else:
                    if 'last_prompt' not in st.session_state:
                        chatbot.start(prompt)
                        st.session_state['last_prompt'] = prompt
                    else:
                        st.session_state['last_prompt'] = prompt
                    if chatbot.get_missing_fields() == []:
                        st.session_state['end'] = True
                        chatbot.user.set_field(chatbot.get_last_field(), st.session_state['last_prompt'])
                        print("Guardando formulario...")
                        chatbot.user.save_user()

            for message in chatbot.get_conversation_history():
                with st.chat_message(message["role"]):
                    st.write(message["content"])
            if(st.session_state['end'] == False and ('consumer_code' in st.session_state.keys() and 'cookie_code' in st.session_state.keys())):
                if chatbot.get_conversation_history()[-1]["role"] != "assistant": 
                    if 'primera_opinion' not in st.session_state.keys():
                        print("USUARIO VA A DAR SU PRIMERA OPINIÓN...")
                        response = chatbot.ask()
                        st.session_state['primera_opinion'] = False
                    else:
                        similarity = embedding.cosine_similarity(embedding.get_embedding(st.session_state['last_prompt']), embedding.get_embedding(chatbot.get_last_field()))
                        if similarity < 0.25:
                            response = chatbot.re_ask()
                        else:
                            print("Guardando datos...")
                            chatbot.user.set_field(chatbot.get_last_field(), st.session_state['last_prompt'])
                            response = chatbot.ask()

                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            st.write(response)    
                            chatbot.add_conversation(role="assistant", content=response) # Add response to message history

if __name__ == "__main__":
    main()   

