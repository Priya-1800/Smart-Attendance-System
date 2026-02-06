import cv2
import numpy as np
import os
import csv
import time
from datetime import datetime
import sys
from whatsapp_sender import send_whatsapp_message
import threading
from sklearn.svm import SVC
from keras_facenet import FaceNet
from win32com.client import Dispatch

attendance_dict = {}   # { "Priya": {"entry": time, "exit": None} }
last_seen = {}         # { "Priya": timestamp }
COOLDOWN = 10          # seconds before allowing another action

CLASS_NAME = os.getenv("CLASS_NAME", "General Class")

# --- Text-to-Speech Setup ---
tts_engine = Dispatch("SAPI.SpVoice")
def speak(text):
    tts_engine.Speak(text)
# ----------------------------

# --- FaceNet and Classifier Setup ---
embedder = FaceNet()
svm_classifier = SVC(kernel='linear', probability=True)

try:
    with np.load('data/faces_embeddings.npz') as data:
        FACES_EMBEDDINGS = data['embeddings']
        LABELS = data['names']
    
    svm_classifier.fit(FACES_EMBEDDINGS, LABELS)
    print("SVM classifier trained successfully.")
except (FileNotFoundError, IndexError) as e:
    print(f"Error loading data or training classifier: {e}")
    print("Please run `add_faces_facenet.py` first to collect and save embeddings.")
    sys.exit()

# Pre-trained OpenCV DNN face detector.
face_detector_dnn = cv2.dnn.readNetFromCaffe(
    'data/deploy.prototxt', 
    'data/res10_300x300_ssd_iter_140000.caffemodel'
)
# ------------------------------------

video = cv2.VideoCapture(0)
attendance_dict = {}
session_attendance = []
img_bg = cv2.imread("background_img.png")

print("Starting Face Recognition...")

while True:
    ret, frame = video.read()
    if not ret:
        break

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_detector_dnn.setInput(blob)
    detections = face_detector_dnn.forward()
    
    recognized_name = "Unknown"

    for k in range(detections.shape[2]):
        confidence = detections[0, 0, k, 2]

        if confidence > 0.5:
            box = detections[0, 0, k, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            crop_img = frame[startY:endY, startX:endX, :]
            
            if crop_img.size > 0:
                resized_img = cv2.resize(crop_img, (160, 160))
                
                try:
                    embedding = embedder.embeddings(np.expand_dims(resized_img, axis=0))[0]
                    embedding = embedding.reshape(1, -1)
                    
                    prediction = svm_classifier.predict(embedding)
                    
                    probability = svm_classifier.predict_proba(embedding)
                    best_match_prob = np.max(probability)
                    
                    threshold = 0.8  
                    if best_match_prob > threshold:
                        recognized_name = prediction[0]
                    else:
                        recognized_name = "Unknown"
                        
                except Exception as e:
                    print(f"Prediction error: {e}")
                    recognized_name = "Unknown"
            
                # --- Attendance Logic ---
                ts = time.time()
                date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
                timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

            now = time.time()

            if recognized_name != "Unknown":

               if recognized_name not in attendance_dict:
                  # FIRST TIME → ENTRY
                  attendance_dict[recognized_name] = {
                  "entry": timestamp,
                  "exit": None
                  }
                  last_seen[recognized_name] = now
                  attendance_record = f"Entry - {recognized_name} at {timestamp}"
                  speak(f"Welcome {recognized_name}, attendance taken.")

            elif attendance_dict[recognized_name]["exit"] is None:
                 # CHECK COOLDOWN before EXIT
                if now - last_seen.get(recognized_name, 0) > COOLDOWN:
                   attendance_dict[recognized_name]["exit"] = timestamp
                   last_seen[recognized_name] = now
                   attendance_record = f"Exit - {recognized_name} at {timestamp}"
                   speak(f"Goodbye {recognized_name}, exit recorded.")
                else:
                    attendance_record = None

            else:
                attendance_record = None

                    
                if attendance_record: 
                   session_attendance.append(attendance_record)
                        
                   # Write to CSV
                   exist = os.path.isfile(f"Attendance/Attendance_{date}.csv")
                   if exist:
                      with open(f"Attendance/Attendance_{date}.csv", "a", newline='') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([recognized_name, timestamp, attendance_dict[recognized_name]['entry'] if 'entry' in attendance_dict[recognized_name] else '', attendance_record.split(' - ')[0]])
                   else:
                        os.makedirs("Attendance", exist_ok=True)
                        with open(f"Attendance/Attendance_{date}.csv", "w", newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(['NAME', 'TIME', 'ENTRY TIME', 'STATUS'])
                            writer.writerow([recognized_name, timestamp, attendance_dict[recognized_name]['entry'], attendance_record.split(' - ')[0]])

                # --- Visuals ---
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0) if recognized_name != "Unknown" else (0, 0, 255), 2)
                cv2.putText(frame, recognized_name, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if recognized_name != "Unknown" else (0, 0, 255), 2)
    
    frame_resized = cv2.resize(frame, (1366, 636))
    img_bg[131:131 + 636, 0:0 + 1366] = frame_resized

    present_count = len(attendance_dict)
    cv2.putText(img_bg, f"Present: {present_count}", (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

    cv2.imshow("Frame", img_bg)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

# Generate and send the full report when the program closes.
# Mark EXIT for everyone when session ends
exit_time = datetime.now().strftime("%H:%M:%S")

for name in attendance_dict:
    exit_record = f"Exit - {name} at {exit_time}"
    session_attendance.append(exit_record)

    date = datetime.now().strftime("%d-%m-%Y")
    with open(f"Attendance/Attendance_{date}.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, exit_time, attendance_dict[name]["entry"], "Exit"])

# Send WhatsApp report
if session_attendance:
    report_message = f"Attendance Report - {CLASS_NAME}\n\n" + "\n".join(session_attendance)
    send_whatsapp_message("+917410597912", report_message)
