import cv2
import threading
import time
from detection_utils import detect_laser_dot
from config import *

class CameraThread(threading.Thread):
    def __init__(self):
        super().__init__()
        # Use DirectShow to avoid MSMF grabFrame errors on Windows
        self.cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

        self.running = True
        self.status = "OFF"
        self.position = None
        self.frame = None

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                # If camera fails, wait a bit and retry
                time.sleep(0.1)
                continue

            dot, mask = detect_laser_dot(frame, RED_LOWER, RED_UPPER)

            if dot:
                x, y, r = dot  # unpack 3 values correctly
                self.status = "ON"
                self.position = (x, y)
                # Draw detection circle and label
                cv2.circle(frame, (x, y), int(r), (0, 255, 0), 2)
                cv2.putText(frame, f"Laser ON ({x},{y})", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                self.status = "OFF"
                self.position = None
                cv2.putText(frame, "Laser OFF", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            self.frame = frame
            time.sleep(0.05)  # adjust for FPS

    def get_frame(self):
        """Return JPEG-encoded frame for Flask video streaming"""
        if self.frame is None:
            return None
        ret, jpeg = cv2.imencode('.jpg', self.frame)
        return jpeg.tobytes()

    def stop(self):
        self.running = False
        self.cap.release()
