# bootloader_patch.py

import face_recognition
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

model_path = resource_path("Backend/models/shape_predictor_68_face_landmarks.dat")
face_recognition.api.pose_predictor_68_point_model_location = lambda: model_path
