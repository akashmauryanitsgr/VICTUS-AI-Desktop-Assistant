import tkinter as tk
from tkinter import ttk, messagebox
import cv2

import pickle,sys,face_recognition.api,dlib
import os
from PIL import Image, ImageTk
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

predictor_path = resource_path("Backend/models/shape_predictor_68_face_landmarks.dat")
face_recognition.api.pose_predictor_68_point = dlib.shape_predictor(predictor_path)
face_recognition.api.pose_predictor_5_point = dlib.shape_predictor(predictor_path)  # Optional if 5-point used
face_recognition.api.face_detector = dlib.get_frontal_face_detector()
USER_DIR = r"C:\Jarvis\Jarvis\Backend\face_auth\users"
os.makedirs(USER_DIR, exist_ok=True)

class FaceRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Register Face - AI Assistant")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        self.username_var = tk.StringVar()

        # Header
        header = ttk.Label(root, text="Face Registration", font=("Segoe UI", 20, "bold"))
        header.pack(pady=20)

        # Username entry
        user_frame = ttk.Frame(root)
        user_frame.pack(pady=10)
        ttk.Label(user_frame, text="Enter Your Name: ", font=("Segoe UI", 12)).pack(side="left")
        ttk.Entry(user_frame, textvariable=self.username_var, width=25).pack(side="left", padx=5)

        # Video frame
        self.video_label = tk.Label(root, bg="#ccc", width=400, height=300, relief="sunken")
        self.video_label.pack(pady=20)

        # Capture button
        self.capture_btn = ttk.Button(root, text="Capture Face", command=self.capture_face)
        self.capture_btn.pack(pady=10)

        # Start webcam
        self.cap = cv2.VideoCapture(0)
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.last_frame = frame
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            img = img.resize((400, 300))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.root.after(10, self.update_frame)

    def capture_face(self):
        name = self.username_var.get().strip().lower()
        if not name:
            messagebox.showerror("Error", "Please enter a name.")
            return

        rgb_frame = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if not face_locations:
            messagebox.showwarning("No Face Found", "No face detected. Try again.")
            return

        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
        with open(os.path.join(USER_DIR, f"{name}.pkl"), "wb") as f:
            pickle.dump(face_encoding, f)

        messagebox.showinfo("Success", f"Face for '{name}' registered successfully!")

    def on_close(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRegisterApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
