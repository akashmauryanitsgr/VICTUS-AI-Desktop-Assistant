import tkinter as tk
from tkinter import ttk, messagebox
import os, dlib, sys, threading, pickle, cv2
from PIL import Image, ImageTk
from Main import SecondThread, FirstThread
import face_recognition.api

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

predictor_path = resource_path("Backend/models/shape_predictor_68_face_landmarks.dat")
if not os.path.exists(predictor_path):
    raise FileNotFoundError(f"Predictor data file not found at {predictor_path}")
face_recognition.api.pose_predictor_68_point = dlib.shape_predictor(predictor_path)

USER_DIR = resource_path("Backend/face_auth/users")

class FaceUnlockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Unlock - AI Assistant")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        ttk.Label(root, text="Face Unlock", font=("Segoe UI", 22, "bold")).pack(pady=20)

        self.video_label = tk.Label(root, bg="#ccc", width=400, height=300, relief="sunken")
        self.video_label.pack(pady=20)

        self.status_label = ttk.Label(root, text="Initializing...", font=("Segoe UI", 12))
        self.status_label.pack(pady=10)

        self.cap = None
        self.known_encodings = []
        self.known_names = []
        self.initialized = False

        threading.Thread(target=self.initialize_camera_and_encodings, daemon=True).start()
        self.update_frame()

    def initialize_camera_and_encodings(self):
        # Warm up camera
        self.cap = cv2.VideoCapture(0)
        for _ in range(5):
            self.cap.read()

        # Load encodings
        for file in os.listdir(USER_DIR):
            if file.endswith(".pkl"):
                name = file.replace(".pkl", "")
                with open(os.path.join(USER_DIR, file), "rb") as f:
                    encoding = pickle.load(f)
                    self.known_encodings.append(encoding)
                    self.known_names.append(name)

        self.initialized = True
        self.status_label.config(text="Waiting for face...")

    def update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb).resize((400, 300))
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

                if self.initialized:
                    self.detect_and_authenticate(rgb)

        self.root.after(10, self.update_frame)

    def detect_and_authenticate(self, rgb_frame):
        face_locations = face_recognition.face_locations(rgb_frame)
        if not face_locations:
            self.status_label.config(text="No face detected.")
            return

        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding, tolerance=0.5)
            if True in matches:
                name = self.known_names[matches.index(True)]
                self.status_label.config(text=f"Access Granted: Welcome, {name.capitalize()}!", foreground="green")
                self.after_unlock(name)
                threading.Thread(target=FirstThread, daemon=True).start()
                SecondThread()
                return
        self.status_label.config(text="Unauthorized face!", foreground="red")

    def after_unlock(self, username):
        self.cap.release()
        messagebox.showinfo("Unlocked", f"Welcome back, {username.capitalize()}!")
        self.root.destroy()

    def on_close(self):
        if self.cap: self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceUnlockApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
