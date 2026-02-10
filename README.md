# Vocal-Simulink-Architect 🎙️🏗️

An AI-powered framework that generates Simulink models from voice commands. This project leverages NLP to automate system design and block diagram generation via the MATLAB API.

## 🚀 Overview
Traditionally, building Simulink models requires manual dragging and dropping of blocks. This project introduces a **Voice-to-Design** workflow, allowing engineers to describe their system (e.g., "Add a PID controller with a step input") and have the model built automatically.

## 🛠️ Tech Stack
- **AI/NLP:** OpenAI Whisper (Speech-to-Text) / GPT-4 (Intent Parsing).
- **Backend:** Python.
- **Control System Interface:** MATLAB Engine API for Python.
- **Target Environment:** Simulink.

## 📂 Project Structure
- `/app.py`: Main entry point for voice capture and processing.
- `/scripts`: Python-to-MATLAB automation scripts.
- `/models`: Generated Simulink (.slx) examples.

## ⚙️ Installation & Setup
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/mostar81/Vocal-Simulink-Architect.git](https://github.com/mostar81/Vocal-Simulink-Architect.git)