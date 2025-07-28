
import requests
import speech_recognition as sr
import pyttsx3
import time
from camera_manager import CameraManager, monitor_unconsciousness
import threading
# ------------------- SETTINGS -------------------
BACKEND_CHAT_URL   = "http://127.0.0.1:5500/llm_chat"
BACKEND_DEVICE_URL = "http://127.0.0.1:5500/device_control"
BACKEND_DOCTOR_URL = "http://127.0.0.1:5500/nearby_doctors"
CAMERA_INDEX       = 0
emergency_triggered = False
face_last_seen = time.time()
last_alert_time = 0  # ⏱️ New: track when last alert fired


# ------------------- TTS FUNCTION -------------------
tts_lock = threading.Lock()

def speak(text):
    print(f"Bot: {text}")
    try:
        engine = pyttsx3.init('sapi5')
    except:
        engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    with tts_lock:
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    time.sleep(0.5)
# ------------------- VOICE LISTENER -------------------
recognizer = sr.Recognizer()

# assistant.py में

import speech_recognition as sr
recognizer = sr.Recognizer()

def listen():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("🎙️ Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        return recognizer.recognize_google(audio)
    except sr.WaitTimeoutError:
        print("[Mic] No speech detected (timeout).")
        return ""
    except sr.UnknownValueError:
        print("[Mic] Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"[Mic] API unavailable: {e}")
        return ""
    except OSError as e:
        # Catch Stream closed or device errors
        print(f"[Mic] OS error: {e}")
        return ""
    except Exception as e:
        print(f"[Mic] Unexpected error: {e}")
        return ""


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
# ------------------- CALLING FUNCTION -------------------
def make_phone_call(phone_number):
    try:
        import os
        os.system(f'adb shell am start -a android.intent.action.CALL -d tel:{phone_number}')
        speak(f"Calling {phone_number} now.")
    except Exception as e:
        print(f"Error making call: {e}")
        speak("Sorry, I couldn't make the call.")

# ------------------- DOCTOR SUGGESTION -------------------
def suggest_doctor(location_text=None, specialization="doctor"):
    if not location_text:
        speak("Should I suggest nearby doctors?")
        confirmation = listen().lower()
        if not any(k in confirmation for k in ["suggest doctor", "suggest doctors", "yes suggest", "show doctor", "show doctors"]):
            speak("Alright, let me know if you change your mind.")
            return
        speak("Please tell me your location — anyone : city, state, or country.")
        location_text = listen().strip()

    speak("What kind of doctor do you want to find? You can say general, dentist, pediatrician, cardiologist, etc.")
    specialization = listen().strip().lower()
    if specialization == "":
        specialization = "doctor"

    speak(f"Searching for {specialization} near {location_text}")
    try:
        geo_resp = requests.get("https://nominatim.openstreetmap.org/search", params={
            'q': location_text,
            'format': 'json'
        }, headers={'User-Agent': 'FunnyFriendBot/1.0'})
        geo_data = geo_resp.json()
        if not geo_data:
            speak("Sorry, I couldn't find that location. Please try again.")
            return

        lat = geo_data[0]['lat']
        lng = geo_data[0]['lon']
        search_keyword = f"{specialization} doctor"
        payload = {"lat": lat, "lng": lng, "keyword": search_keyword}
        resp = requests.post(BACKEND_DOCTOR_URL, json=payload, timeout=5)
        data = resp.json()
        doctors = data.get("results", [])

        if not doctors:
            speak(f"Sorry, I couldn't find any {specialization} near {location_text}.")
            return

        speak(f"Here are some {specialization} options near you:")
        for index, doc in enumerate(doctors[:3]):
            name = doc.get("name", "Unknown clinic")
            rating = doc.get("rating", "no rating")
            address = doc.get("vicinity", "no address listed")
            phone = doc.get("phone", "no phone number available")
            speak(f"{index + 1}. {name}, rated {rating}, at {address}. Contact: {phone}.")

        speak("Would you like me to call any of these doctors?")
        response = listen().lower()
        word_to_digit = {
            "first": "1", "1": "1", "one": "1",
            "second": "2", "2": "2", "two": "2",
            "third": "3", "3": "3", "three": "3"
        }

        selected_index = None
        for word, digit in word_to_digit.items():
            if f"call {word}" in response or f"number {word}" in response or word in response:
                selected_index = int(digit) - 1
                break

        if selected_index is not None and 0 <= selected_index < len(doctors):
            selected = doctors[selected_index]
            phone_number = selected.get("phone", "")
            if phone_number and "no" not in phone_number.lower():
                make_phone_call(phone_number)
            else:
                speak("This doctor does not have a phone number listed.")
            return

        if any(k in response for k in ["yes", "call", "dial", "doctor", "number"]):
            speak("Please say the number — first, second, or third doctor.")
            choice = listen().lower()
            for word, digit in word_to_digit.items():
                if word in choice:
                    selected_index = int(digit) - 1
                    break
            if selected_index is not None and 0 <= selected_index < len(doctors):
                selected = doctors[selected_index]
                phone_number = selected.get("phone", "")
                if phone_number and "no" not in phone_number.lower():
                    make_phone_call(phone_number)
                else:
                    speak("This doctor does not have a phone number listed.")
            else:
                speak("Sorry, I didn't catch which doctor to call.")
        else:
            speak("Okay, no call will be made.")

    except Exception as e:
        print("Error in location-based doctor search:", e)
        speak("Sorry, I ran into trouble finding doctors.")

# ------------------- MAIN ASSISTANT -------------------
def main():
    speak("Hello! I'm your Funny Friend AI.")
    speak("Before we begin, how are you feeling today?")
    time.sleep(0.5)
    emotion = listen().lower().strip()
    print(f"Detected emotion from voice: {emotion}")

    # Emergency emotion response
    if any(e in emotion for e in ["sad", "depressed", "angry", "anxious", "fear", "disgust"]):
        speak("You sound a bit low. Are you okay?")
        time.sleep(0.5)
        response = listen().lower()
        if any(word in response for word in ["no", "not fine", "bad", "hurt", "pain", "sad"]):
            suggest_doctor()
        else:
            speak("Okay, glad you're managing.")

    doctor_mode = False
    location_collected = False
    specialization_collected = False
    location_text = ""
    specialization = ""

    while True:
        text = listen().strip()
        if not text:
            continue
        print(f"You: {text}")

        if text.lower() in ("exit", "quit", "bye"):
            speak("Goodbye! Take care.")
            time.sleep(0.5)
            break

        if any(d in text.lower() for d in ["fan", "light", "ac", "tv", "curtain", "party", "music"]):
            control_device(text)
            continue

        if any(k in text.lower() for k in ["doctor", "doctors", "nearby doctor", "psychiatrist", "clinic"]):
            doctor_mode = True
            location_collected = False
            specialization_collected = False
            speak("Should I suggest nearby doctors?")
            time.sleep(0.5)
            confirmation = listen().lower()
            if any(k in confirmation for k in ["suggest doctor", "suggest doctors", "yes suggest", "show doctor", "show doctors"]):
                speak("Please tell me your location — anyone : city, state, or country.")
                time.sleep(0.5)
            else:
                speak("Alright, let me know if you change your mind.")
                time.sleep(0.5)
                doctor_mode = False
            continue

        if doctor_mode and not location_collected:
            location_text = text
            location_collected = True
            speak( " tell once more")
            continue

        if doctor_mode and location_collected and not specialization_collected:
            specialization = text
            specialization_collected = True
            suggest_doctor(location_text=location_text, specialization=specialization)
            doctor_mode = False
            continue

        try:
            prompt = f"User is feeling {emotion}. They said: '{text}'. Respond kindly."
            reply = requests.post(BACKEND_CHAT_URL, json={"prompt": prompt}).json().get("reply", "")
        except:
            reply = "Chat service unavailable."
        speak(reply)

# ------------------- UNCONSCIOUSNESS MONITOR -------------------
if __name__ == "__main__":
    def emergency_alert():
        global emergency_triggered
        if emergency_triggered:
            return
        emergency_triggered = True

        speak("🚨 Emergency detected! Please respond or I will notify your contact.")
        time.sleep(3)
        response = listen().lower()

        if any(k in response for k in ["i am fine", "i'm fine", "cancel", "not emergency"]):
            speak("Okay, staying alert but not calling anyone.")
            time.sleep(0.5)
            emergency_triggered = False
            return

        print("📞 Simulating emergency call...")
        speak("Calling emergency contact now. Please stay calm, help is on the way.")
        time.sleep(0.5)

        emergency_triggered = False  # ✅ Reset so future emergencies can be triggered


    if __name__ == "__main__":
        camera_manager = CameraManager()

        # Start monitoring in background
        monitoring_thread = threading.Thread(
            target=monitor_unconsciousness,
            args=(camera_manager, 150, emergency_alert),
            daemon=True
        )
        monitoring_thread.start()

        main()

