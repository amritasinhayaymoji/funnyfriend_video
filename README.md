# Funny Friend (Video Prototype) 🎥

*Facial Emotion → AI Chat → Smart Device Control*
**Future Vision of the Funny Friend Project**

This is a backend-only prototype of Funny Friend — a smart AI assistant that reads your emotions through webcam, chats with you using LLM, and controls devices like lights and fans.
It’s designed as a **future version** of the main web app (Funny Friend Web), with no frontend — only webcam + voice + backend magic.

> 📝 This is not part of the Google Developer Challenge submission, but is featured in the YouTube demo as a **"what’s next"** showcase.

---

## 🎯 What It Can Do

| Feature                           | Description                                                           |
| --------------------------------- | --------------------------------------------------------------------- |
| 👀 Facial Emotion Detection       | Detects your mood in real-time using webcam and DeepFace              |
| 🧠 Emotion-Aware AI Chat          | Starts conversation using OpenRouter LLM, based on your detected mood |
| 💡 Smart Device Control           | Controls light/fan via Flask API routes (simulated IoT control)       |
| 🖥️ Voice Interaction in Terminal | Uses mic input + speech output — no browser required                  |
| 🔗 Linked in Demo Video           | Shown inside the YouTube demo of the main Funny Friend web app        |

---

## 🛠 How to Run (Two-Terminal Setup)

> ✅ Requirements: Python 3.8+, webcam, microphone, internet

### 🔹 Step 1: Clone and Install

```bash
git clone https://github.com/yourusername/funny_friend-video.git
cd funny_friend-video
pip install -r requirements.txt
```

### 🖥️ Terminal 1: Start Flask Backend (Device Control)

This will run the backend Flask server on port 5500.

```bash
python app.py
# Server will run at: http://localhost:5500
```

### 🧠 Terminal 2: Run Voice Assistant (Emotion + LLM)

This starts the voice assistant loop — it listens, detects emotion from your face, and replies via LLM.

```bash
python assistant.py
```

### 🎤 Just speak naturally. The assistant will:

* Detect your facial emotion from webcam
* Decide how to respond (chat or device control)
* Speak the response using TTS

---

## 🔧 Tech Stack

* **Python (Flask)** – Backend for API and device control
* **DeepFace** – Webcam-based facial emotion detection
* **SpeechRecognition + Pyttsx3** – Voice input/output via terminal
* **OpenRouter API** – Large Language Model for conversations
* **Custom APIs** – Fan and Light control routes (`/device_control`)
* **No Frontend** – All backend & terminal driven
* **Port** – App runs on `http://localhost:5500`

---

## 🔍 Ideal Use Cases

This backend version is designed for:

* Smart mirrors or wall displays
* Raspberry Pi setups
* Kiosk assistants
* Emotion-aware embedded systems
* Mental health or wellness bots

---

## 📹 Demo & Context

This project is shown in the YouTube demo of our official competition submission:

* 🔗 **Main Project**: Funny Friend Web
* 📺 **Watch Full Demo Video**: YouTube Link

---

## 📝 For Judges

This repo is not submitted in the official Google Home API Developer Challenge.
It’s shown in the demo video to highlight the next-level potential of the Funny Friend assistant — moving beyond browser into real-world smart interfaces.
🌐 Browser-based implementation was not used in this prototype to allow deeper system-level integration (e.g., webcam, real-time device control). This backend-first 
  approach enabled smoother testing of AI and hardware workflows beyond browser limits.
We hope it offers a glimpse into the future direction of emotional AI assistants.

---

## 👩‍💻 Created By

**Funny Friend Project Series**
By \[Your Name]
🔗 GitHub: [https://github.com/yourusername](https://github.com/yourusername)
📧 Email: [yourname@email.com](mailto:yourname@email.com)

Built with ❤️ to imagine AI that truly understands and responds to how we feel.