🎥 Funny Friend (Video Prototype)
Real-Time Monitoring → Emotion Chat → Smart Control – Future Vision of the Funny Friend Project

This is a backend-only prototype of Funny Friend — an empathetic AI assistant built especially for those who are alone, elderly, or unwell.

It uses your webcam and voice to:

Monitor for emergencies like unconsciousness using live camera feed

Detect emotions from your voice and monitor live webcam for unconsciousness

Trigger an emergency alert and simulate phone calls automatically

Offer emotion-aware conversations using an LLM

Control smart home devices (like fans and lights)

Suggest nearby doctors based on location and emotion, with call simulation

It also engages in funny or empathetic chats, depending on your mood.

🚫 Note: This prototype runs entirely outside the browser because web browsers restrict access to real-time camera feeds, making deep integration impossible in a web-only environment.

---

## 🎯 What It Can Do
| Feature                             | Description                                                                                                                                                  |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 👁️ Real-Time Emergency Detection   | Continuously monitors webcam feed. If no face is detected for several seconds, it triggers an **emergency alert** and **simulates an emergency call**.       |
| 🧠 Emotion Detection (Voice & Face) | Detects how you're feeling using both your **voice input** and **facial expressions** via live camera.                                                       |
| 💬 Emotion-Aware AI Chat            | Starts a personalized conversation using **OpenRouter LLM** based on detected emotion (like anxiety, sadness, anger).                                        |
| 👩‍⚕️ Nearby Doctor Suggestions     | Based on your **location and emotional state**, it suggests doctors nearby and even offers to **simulate a phone call**.                                     |
| 💡 Smart Device Control             | Turns devices like **fans, lights, or curtains** on/off using natural voice commands (simulated IoT control).                                                |
| 🔊 Voice Interaction Only           | Fully functional via **mic input and TTS output** — no mouse, no screen — perfect for elderly or bedridden users.                                            |
| 🖥️ Terminal-Based Assistant        | Runs completely in terminal using **Python**, enabling tighter system access like camera/mic that browsers can’t provide.                                    |
| 🚫 Browser-Free for Deeper Access   | Camera access is **not allowed in browser** environments — this backend setup enables **real-time AI monitoring** and device control beyond web limitations. |
| 🧓 Built for Elderly, Sick, Alone   | Designed for users who might be living alone or need **mental health and emergency support**, even when no one is around.                                    |

---

## 🛠️ How to Run (Two-Terminal Setup)

### ✅ Requirements
- Python 3.8+  
- Webcam  
- Microphone  
- Internet connection  
- ADB (optional for Android phone call trigger)

---


### 🔹 Step 1: Clone and Install

```bash
git clone https://github.com/amritasinhayaymoji/funnyfriend_video.git
cd funnyfriend_video
pip install -r requirements.txt
```

### 🖥️ Terminal 1: Start Flask Backend (Device Control)

This will run the backend Flask server on port 5500.

```bash
python app.py
# Server will run at: http://localhost:5500
```

### 🧠 Terminal 2: Run Voice Assistant (Emotion + LLM)

This starts the assistant loop — it listens to your voice, detects your emotion, and replies using LLM.

```bash
python assistant.py
```

🎤 Just Speak Naturally – Here's What the Assistant Does:
👁️ Uses live webcam to monitor for unconsciousness or absence

💬 Asks how you’re feeling (voice input)

😊 Detects emotion from your spoken words

🧑‍⚕️ Suggests nearby doctors based on your location and mood

📞 Can simulate an emergency call or call to doctors

💡 Understands commands like “turn on the light” or “fan off”

🤖 Chats kindly with you using LLM-based responses

🗣️ Speaks back using text-to-speech (TTS)

---

| Technology     | Purpose        |
| -------------- | -------------- |
| **Python**     | Main programming language |
| **Flask**      | Backend server and API routes |
| **OpenRouter API** | LLM-based empathetic conversation |                
| **SpeechRecognition** | Voice input    |
| **Pyttsx3**    | Voice output (TTS) |
| **OpenCV**     | Webcam feed + face detection |
| **Threading**  | Background face monitoring |
| **Joblib**     | (Optional) Emotion model serialization |
| **dotenv**     | For securing API keys |
| **CORS**       | Flask CORS support |
| **ADB**        | Optional — simulate call via Android device |


### 💡 Ideal Use Cases
This prototype is built for:

Smart mirrors or bathroom assistants

Raspberry Pi emotion bots

Wellness/mental-health kiosks

AI assistants for the elderly

Emotion-driven device control (lights/fans/music)



## 📹 Demo & Context

This project is shown in the YouTube demo of our official competition submission:

* 🔗 **Main Project**: https://github.com/amritasinhayaymoji/funnyfriend.git
* 📺 **Watch Full Demo Video**: https://youtu.be/5X4x4VMHWZk

---

## 📝 For Judges

This repository showcases the extended prototype of Funny Friend: Yaymoji, submitted alongside the main browser-based version.

It demonstrates advanced features like emergency detection and device control using voice and camera — built as a backend-first system to overcome browser limitations (e.g., webcam access, real-time hardware interaction).

While the primary browser version supports most functionality, this prototype highlights how Funny Friend can evolve into a real-world smart assistant beyond the browser.

Together, both versions show the scalable potential of emotional AI, from web to home environments.

---

## 👩‍💻 Created By

**Funny Friend Project Series**  
**By:** *Amrita Sinha*  
🔗 **Prototype GitHub:** [Funny Friend – Video Assistant](https://github.com/amritasinhayaymoji/funnyfriend_video.git)  
🔗 **Main Project:** [Funny Friend – Web Version](https://github.com/amritasinhayaymoji/funnyfriend)  
📧 **Email:** amritasinha.yaymoji@gmail.com  

Built with ❤️ to imagine AI that truly understands and responds to how we feel.
---
### 🧪 Note on Free Tools Used

This prototype is built entirely using free-tier APIs and open-source libraries. No paid tools were used.
With premium access (e.g., GPT-4, cloud AI, or Dialogflow CX), performance and accuracy can be significantly enhanced.