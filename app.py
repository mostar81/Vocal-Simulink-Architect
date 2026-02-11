import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
# ... (garde ton code de configuration de la clé API ici) ...
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Utilisation de Gemini 2.5
model=genai.GenerativeModel("models/gemini-2.5-flash")

#interface Streamlit pour transformer python en web
st.set_page_config(page_title="Simulink Voice AI", page_icon="🎙️")
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
    with st.spinner("Analyse de votre demande orale et dessin du circuit..."):
        #on prépare l'audio pour Gemini
        audio_data={"mime_type":"audio/wav","data":audio['bytes']}
        #on demande à Gemini de transformer l'audio en texte, Code Matlab et code Graphviz
        #La première version était: transcription_response = model.generate_content(["Retranscris exactement ce que dit cet audio, sans rien ajouter :", audio_data])
        prompt_instruction=(
            "Analyse cet audio. Réponds en suivant strictement ce plan :\n"
            "1. Transcription : [Texte de la transcription]\n"
            "2. Code MATLAB : Génère le code Simulink (new_system, add_block, add_line).\n"
            "3. Visualisation : Génère un code Graphviz DOT (digraph { ... }) pour dessiner ce circuit.\n"
            "Utilise des blocs de code Markdown (```matlab et ```graphviz)."
        )

        try:
            # Appel unique à l'API
            response = model.generate_content([prompt_instruction, audio_data])
            full_response = response.text
            # 1. Extraction de la Transcription
            transcription = full_response.split("2.")[0].replace("1. Transcription :", "").strip()

            # 2. Extraction du code MATLAB
            matlab_match = re.search(r"```matlab\n(.*?)```", full_response, re.DOTALL)
            matlab_code = matlab_match.group(1) if matlab_match else "Code MATLAB non généré."

            # 3. Extraction du code Graphviz
            graphviz_match = re.search(r"```graphviz\n(.*?)```", full_response, re.DOTALL)
            dot_code = graphviz_match.group(1) if graphviz_match else None

            # --- AFFICHAGE DES RÉSULTATS ---
            st.subheader("📝 Ce que j'ai compris :")
            st.info(transcription)

            # Affichage du schéma dessiné
            if dot_code:
                st.subheader("📊 Schéma du circuit :")
                st.graphviz_chart(dot_code)

            # Affichage du code MATLAB
            st.subheader("💻 Code MATLAB / Simulink :")
            st.code(matlab_code, language='matlab')

            # Bouton pour télécharger le code
            st.download_button(
                label="Télécharger le script .m",
                data=matlab_code,
                file_name="circuit_simulink.m",
                mime="text/x-matlab"
            )
        except Exception as e:
            set.error(f"Une erreur est survenue: {e}")


        # l'ancienne version: user_message=transcription_response.text
        #afficher le message compris dans un box
        #st.subheader("ce que j'ai compris:")
        #st.info(user_message)
         #on éfinit la consigne (Prompt)
        #prompt_instruction=(
           # "Analyse cet audio. 1) Retranscris ce que l'utilisateur demande."
          #  "2) Génère uniquement le code MATLAB/Simulink(fonctions add_block, add_line)"
          #  "pour réaliser ce circuit"
       # )
        # on envoie la liste à Gemini [consigne, Audio]
        #response = model.generate_content([prompt_instruction, audio_data])
        #affichage du résultat
        #st.subheader("Solution Simulink généré :")
        #st.code(response.text)