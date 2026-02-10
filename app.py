import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
from dotenv import load_dotenv
import os
# ... (garde ton code de configuration de la clé API ici) ...
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("models/gemini-2.5-flash")
#interface Streamlit pour transformer python en web
st.title("🎙️ Simulink Voice AI")
st.write("Dites-moi quel circuit vous souhaitez générer.")

# Création du bouton d'enregistrement
audio = mic_recorder(
    start_prompt="Cliquez pour parler 🎤",
    stop_prompt="Arrêter l'enregistrement ⏹️",
    key='recorder'
)

if audio:
    # On récupère l'audio (ici on suppose que tu l'envoies à Gemini pour transcription)
    # Pour un test rapide, on peut aussi utiliser un champ texte en attendant
    with st.spinner("Analyse de votre demande orale..."):
        #on prépare l'audio pour Gemini
        audio_data={"mime_type":"audio/wav","data":audio['bytes']}
        #on demande à Gemini de transformer l'audio en texte
        transcription_response = model.generate_content(["Retranscris exactement ce que dit cet audio, sans rien ajouter :", audio_data])
        user_message=transcription_response.text
        #afficher le message compris dans un box
        st.subheader("ce que j'ai compris:")
        st.info(user_message)
         #on éfinit la consigne (Prompt)
        prompt_instruction=(
            "Analyse cet audio. 1) Retranscris ce que l'utilisateur demande."
            "2) Génère uniquement le code MATLAB/Simulink(fonctions add_block, add_line)"
            "pour réaliser ce circuit"
        )
        # on envoie la liste à Gemini [consigne, Audio]
        response = model.generate_content([prompt_instruction, audio_data])
        #affichage du résultat
        st.subheader("Solution Simulink généré :")
        st.code(response.text)