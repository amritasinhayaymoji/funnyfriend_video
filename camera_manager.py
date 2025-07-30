import cv2
import threading
import time

class CameraManager:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.lock = threading.Lock()
        self.in_use = False

    def start_camera(self):
        with self.lock:
            if not self.in_use:
                # -----------------------------------------
                # Use DirectShow backend on Windows:
                # -----------------------------------------
                self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
                if not self.cap.isOpened():
                    raise Exception("Cannot open camera (DirectShow)")
                self.in_use = True
                return self.cap
            else:
                raise Exception("Camera already in use")

    def release_camera(self):
        with self.lock:
            if self.cap and self.in_use:
                self.cap.release()
                self.in_use = False

    def is_in_use(self):
        with self.lock:
            return self.in_use

    def read_frame(self):
        with self.lock:
            if self.cap and self.in_use:
                ret, frame = self.cap.read()
                if not ret:
                    raise Exception("Failed to grab frame")
                return frame
            else:
                raise Exception("Camera not started or already released")

# ---------- Test Camera Manually ----------
def test_camera():
    camera_manager = CameraManager()
    try:
        camera_manager.start_camera()
    except Exception as e:
        print(f"Error starting camera: {e}")
        return

    print("Camera started. Press 'q' to quit.")
    while True:
        try:
            frame = camera_manager.read_frame()
        except Exception as e:
            print(f"Error reading frame: {e}")
            break

        cv2.imshow("Camera Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera_manager.release_camera()
    cv2.destroyAllWindows()

# ---------- Monitor for Unconsciousness ----------
def monitor_unconsciousness(camera_manager, threshold_seconds=20, callback=None):
    import assistant  # Access shared state
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    try:
        camera_manager.start_camera()
    except Exception as e:
        print(f"Monitor start error: {e}")
        return

    while True:
        try:
            frame = camera_manager.read_frame()
        except:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            assistant.face_last_seen = time.time()
            if assistant.emergency_triggered:
                print("👀 Face reappeared, resetting emergency.")
                assistant.emergency_triggered = False
        else:
            if time.time() - assistant.face_last_seen > threshold_seconds:
                if not assistant.emergency_triggered and callback:
                    assistant.last_alert_time = time.time()  # ⏱️
                    callback()

                # 🔁 Reset trigger after 30 seconds of alert, even if no face
                elif assistant.emergency_triggered and (time.time() - assistant.last_alert_time > 20):
                    print("🔁 Resetting emergency trigger after timeout.")
                    assistant.emergency_triggered = False

        time.sleep(1)

    camera_manager.release_camera()


# ---------- Entry Point ----------
if __name__ == "__main__":
    test_camera()
