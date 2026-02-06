import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import os
import sys
import tkinter.messagebox as mb
import cv2

USER = os.getenv("LOGGED_USER", "default_user")
BASE_DIR = f"users/{USER}"
ATTENDANCE_DIR = f"{BASE_DIR}/Attendance"
DATA_DIR = f"{BASE_DIR}/data"

os.makedirs(ATTENDANCE_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

process = None
cap = None

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Attendance System")
app.geometry("700x600")

# ========== FUNCTIONS ==========

def start_camera_preview():
    global cap
    cap = cv2.VideoCapture(0)
    show_frame()

def show_frame():
    if cap is None:
        return
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (300, 220))
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        camera_label.imgtk = img
        camera_label.configure(image=img)
    camera_label.after(10, show_frame)

def capture_faces():
    name = name_entry.get()
    if not name:
        status_label.configure(text="⚠ Please enter a name", text_color="red")
        return
    os.environ["PERSON_NAME"] = name
    subprocess.Popen([sys.executable, "add_faces_facenet.py"])
    status_label.configure(text=f"📸 Capturing faces for {name}", text_color="lightgreen")

def start_attendance():
    global process
    subject = subject_entry.get()
    if not subject:
        status_label.configure(text="⚠ Enter Subject / Class name", text_color="red")
        return
    os.environ["CLASS_NAME"] = subject
    process = subprocess.Popen([sys.executable, "test.py"])
    status_label.configure(text=f"▶ Session Started: {subject}", text_color="lightgreen")

def end_session():
    global process
    if process:
        process.terminate()
        process = None
        status_label.configure(text="⏹ Session Ended.", text_color="orange")
    else:
        status_label.configure(text="ℹ No active session running.", text_color="yellow")

def toggle_theme():
    current = ctk.get_appearance_mode()
    ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")

# ========== IMAGES ==========

logo_img = ctk.CTkImage(Image.open("assets/logo.png"), size=(100,100))
camera_icon = ctk.CTkImage(Image.open("assets/camera.png"), size=(24,24))
start_icon = ctk.CTkImage(Image.open("assets/start.png"), size=(24,24))
stop_icon = ctk.CTkImage(Image.open("assets/stop.png"), size=(24,24))

# ========== UI ==========

top_frame = ctk.CTkFrame(app)
top_frame.pack(fill="x", pady=10)

ctk.CTkLabel(top_frame, image=logo_img, text="").pack(side="left", padx=15)
ctk.CTkLabel(top_frame, text="Smart Face Attendance System", font=("Segoe UI", 20, "bold")).pack(side="left")

middle_frame = ctk.CTkFrame(app)
middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

left_panel = ctk.CTkFrame(middle_frame)
left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="n")

right_panel = ctk.CTkFrame(middle_frame)
right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="n")

# Left Panel
ctk.CTkLabel(left_panel, text="Face Registration", font=("Segoe UI", 16, "bold")).pack(pady=10)
name_entry = ctk.CTkEntry(left_panel, placeholder_text="Enter Student Name", width=220)
name_entry.pack(pady=8)
ctk.CTkButton(left_panel, text=" Capture Faces", image=camera_icon, command=capture_faces, width=220).pack(pady=6)

# Right Panel
ctk.CTkLabel(right_panel, text="Live Camera Preview", font=("Segoe UI", 16, "bold")).pack(pady=10)

camera_label = ctk.CTkLabel(right_panel, text="")
camera_label.pack(pady=5)

subject_entry = ctk.CTkEntry(right_panel, placeholder_text="Enter Subject / Class Name", width=220)
subject_entry.pack(pady=8)

ctk.CTkButton(right_panel, text=" Start Attendance", image=start_icon, command=start_attendance, width=220).pack(pady=6)
ctk.CTkButton(right_panel, text=" End Session", image=stop_icon, command=end_session, width=220, fg_color="red").pack(pady=6)

# Bottom
ctk.CTkButton(app, text=" 🌗 Toggle Theme", command=toggle_theme, width=200).pack(pady=10)

status_label = ctk.CTkLabel(app, text="Ready.", font=("Segoe UI", 14))
status_label.pack(pady=10)

start_camera_preview()
app.mainloop()




