import cv2
import requests
import speech_recognition as sr
import pyttsx3
from deepface import DeepFace
import time

# ------------------- SETTINGS -------------------
BACKEND_CHAT_URL   = "http://127.0.0.1:5500/llm_chat"
BACKEND_DEVICE_URL = "http://127.0.0.1:5500/device_control"
CAMERA_INDEX       = 0

# ------------------- TTS FUNCTION -------------------
def speak(text):

    print(f"Bot: {text}")
    try:
        engine = pyttsx3.init('sapi5')
    except:
        engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.2)

# ------------------- VOICE LISTENER -------------------
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("🎙️ Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            return recognizer.recognize_google(audio)
        except:
            return ""

# ------------------- EMOTION DETECTION -------------------
def detect_emotion(frame):
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        print(result)
        return (result[0]['dominant_emotion']
                if isinstance(result, list)
                else result['dominant_emotion'])
    except Exception as e:
        print("Emotion detection error:", e)
        return "neutral"

# ------------------- DEVICE CONTROL -------------------
def control_device(cmd):
    try:
        resp = requests.post(BACKEND_DEVICE_URL, json={"text": cmd}).json()
        if resp.get("success"):
            speak(f"{resp['device'].capitalize()} turned {resp['action']}.")
        else:
            speak("Device command not recognized.")
    except:
        speak("Device service error.")

# ------------------- MAIN ASSISTANT -------------------
def main():

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        speak("Camera unavailable.")
        return

    speak("Starting camera. Please look here.")
    time.sleep(1)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        speak("Could not capture frame.")
        return


    cv2.imshow("Preview", frame)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()


    speak("Hello! Nice to see you.")
    emotion = detect_emotion(frame)
    print(f"Detected emotion: {emotion}")

    # 3️⃣ chat and device control
    while True:
        text = listen().strip()
        if not text:
            continue
        print(f"You: {text}")

        if text.lower() in ("exit", "quit", "bye"):
            speak("Goodbye! Take care.")
            break

        # device commands
        if any(d in text.lower() for d in ["fan", "light", "ac", "tv", "curtain", "party"]):
            control_device(text)

        else:
            # LLM chat with detected emotion context
            try:
                reply = requests.post(
                    BACKEND_CHAT_URL,
                    json={"prompt": f"My emotion is {emotion}. User says: {text}"}
                ).json().get("reply", "")
            except:
                reply = "Chat service unavailable."
            speak(reply)

if __name__ == "__main__":
    main()
