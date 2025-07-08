# MedSense – AI Health Companion (Totally a Group Project)

**MedSense** is an AI-powered healthcare assistant built with Streamlit and LangChain. It provides interactive, symptom-based consultations, generates structured medical reports, and offers a clean conversational interface to help users better understand their health. Oh, and it's just getting started.

---

## ✨ Features

* Conversational health assistant powered by LLMs (Mistral)
* Real-time symptom analysis and contextual Q\&A
* Generates detailed consultation reports in Markdown
* Downloadable, timestamped reports for sharing with professionals
* Persistent chat memory per consultation session
* Sidebar controls for session management and disclaimer handling

---

## 🚀 Upcoming Features (for the full MedSense experience)

* **Personalized Medical Chatbot** with medical profile memory
* **Live Camera Health Tools**:

  * Posture detection & back-care feedback (OpenCV + Mediapipe)
  * Blink-rate detection for eye strain assessment
  * Ambient noise analysis for ear health awareness
* **Health Tracker Dashboard** with weekly reports
* **Doctor Mode** to accept report documents & visualize case history
* **Emergency Protocol Detection** (e.g. stroke, heart attack, etc.)
* **Multi-language support** for accessibility
* **User accounts + session history** (Auth + DB storage)

---

## ⚙️ How to Run It

```bash
git clone https://github.com/your-username/medsense
cd medsense
streamlit run app.py
```

Set your API key in `.env`:

```env
MISTRAL_API_KEY=your_api_key_here
```

Dependencies (use `requirements.txt` or `environment.yaml`):

* Streamlit
* LangChain
* ChatMistralAI
* Python-dotenv
* uuid, datetime, markdown

---

## 🔍 File Structure

```bash
medsense/
├── app.py                   # Streamlit frontend
├── agent/
│   ├── __init__.py
│   ├── doctor_agent.py      # LangChain-powered agent logic
│   └── prompts.py           # System prompt and report template
├── utils/
│   ├── __init__.py
│   └── report.py            # Markdown formatter and file saver
├── data/
│   └── medical_knowledge.json  # Common symptoms & home remedies
├── templates/               # HTML UI (if extended)
├── static/                  # For styles/scripts if needed
├── requirements.txt / environment.yaml
└── .env
```

---

## 🚨 Disclaimers

* This app is **not** a substitute for medical advice.
* It doesn’t diagnose, it suggests based on symptom inputs.
* It encourages users to follow up with real doctors (who aren't built from `pip install`).

---

## 💬 Sample Prompt Logic

The system prompt ensures:

* Collection of symptoms through natural conversation
* Identification of potential non-emergency conditions
* Suggests at-home care + when to see a real doctor
* Flags emergency symptoms (e.g. chest pain, stroke, etc.)

Report includes:

* Timestamped consultation ID
* Symptoms
* Possible conditions
* Recommendations
* Friendly legal disclaimer so no one sues you :)

---

## 💼 License

MIT License

---

## 🙏 Acknowledgments

* Mistral AI for powering the diagnosis assistant
* LangChain for the conversational logic
* Streamlit for the rapid UI setup

> You can call it a "proof of concept" or you can call it what it is: a health-tech MVP disguised as coursework.

---
