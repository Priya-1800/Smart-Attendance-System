# 🎯 Smart Face Attendance System (AI Powered)

An AI-based Smart Attendance System using Face Recognition with a modern UI, secure login, and automation features like WhatsApp reporting and Email OTP reset.

---

## 🚀 Features

✔ Face Recognition Attendance (FaceNet + SVM)  
✔ Real-time Camera & UI Preview  
✔ Secure Login & Registration (Hashed Passwords)  
✔ Role-Based Access (Teacher / Staff / HOD)  
✔ Admin Panel (View All Users)  
✔ Email OTP Password Reset  
✔ WhatsApp Attendance Reports  
✔ CSV Attendance Logs  
✔ Modern Desktop UI (CustomTkinter)  

---

## 🛠 Tech Stack

- Python  
- OpenCV  
- FaceNet (keras-facenet)  
- scikit-learn (SVM)  
- CustomTkinter  
- NumPy, Pandas  
- bcrypt (Password Hashing)  
- yagmail (Email OTP)  

---

## 📸 Screenshots

(Add screenshots here once you upload them)

---

---
Smart-Attendance-System/
│
├── assets/                         # UI icons, images, logo, backgrounds
│   ├── logo.png
│   ├── bg.png
│   ├── camera.png
│   ├── start.png
│   ├── stop.png
│   ├── folder.png
│   ├── csv.png
│   ├── clear.png
│   ├── settings.png
│   └── help.png
│
├── users/                          # All registered users (role-based)
│   └── <username>/
│       ├── profile.json           # User profile (role, email, created date)
│       ├── settings.json          # User preferences (camera, threshold, etc.)
│       └── Attendance/            # Attendance CSV files per user
│           └── Attendance_06-02-2026.csv
│
├── data/                           # Face models & embeddings
│   ├── deploy.prototxt            # OpenCV DNN face detector config
│   ├── res10_300x300_ssd_iter_140000.caffemodel  # Face detector model
│   └── faces_embeddings.npz       # Saved FaceNet embeddings
│
├── Attendance/                    # (Optional) Global attendance folder
│   └── Attendance_06-02-2026.csv
│
├── ui_app.py                      # Main UI (Camera preview + buttons + controls)
├── login.py                       # Login screen (secure + role-based)
├── register.py                    # Registration screen
├── admin_panel.py                # Admin/HOD panel (view all users)
├── email_otp_reset.py            # Email OTP password reset system
│
├── add_faces_facenet.py           # Collect & save new face embeddings
├── test.py                        # Core recognition + attendance logic
├── whatsapp_sender.py             # Sends attendance report via WhatsApp
│
├── users_db.json                  # User database (hashed passwords + roles + emails)
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
---

## ⚙️ Installation  

### 1️⃣ Clone Repository  
```bash
git clone https://github.com/yourusername/Smart-Attendance-System.git
cd Smart-Attendance-System
```

### 2️⃣ Create Virtual Environment  
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
```

### 3️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

📌 Example `requirements.txt`:
```
opencv-python
deepface
mtcnn
tensorflow
pywhatkit
pandas
```

---

🧑‍💻 Usage

Step 1: Register & Login
```bash
python register.py
python login.py
```
• Register as Teacher / Staff / HOD
• Login securely (hashed passwords)
• Email OTP system available for password reset

Step 2: Capture Face Embeddings
```bash
python ui_app.py
```
• Enter student name
• Click 📷 Capture Faces
• System captures ~100 embeddings using FaceNet
• Saved in data/faces_embeddings.npz

Step 3: Start Attendance Session

• Enter Subject / Class Name
• Click ▶ Start Attendance
• Real-time camera preview + recognition
• Entry + Exit recorded automatically

Step 4: Reports & Automation

✔ CSV saved per user
✔ WhatsApp report sent automatically
✔ Data stored in:
```bash
users/<username>/Attendance/
```

🧠 Face Recognition Model

This project uses:

• FaceNet for face embeddings
• SVM (scikit-learn) for classification
• OpenCV DNN SSD for face detection

Pipeline:
Camera → DNN Face Detector → FaceNet → SVM → Attendance

🔧 Troubleshooting

• Camera not opening?
Check camera index in settings

• TensorFlow / NumPy issues?
```bash
pip install numpy==1.24.4
pip install tensorflow==2.11.0
```
• WhatsApp not sending?
✔ Make sure WhatsApp Web is logged in
✔ Chrome must be open

• OTP email not sent?
✔ Enable Gmail 2-Step Verification
✔ Use App Password

📌 Future Enhancements

• 📊 Attendance Analytics Dashboard
• 📄 PDF Export Reports
• ☁️ Cloud DB (SQLite / MySQL / Firebase)
• 🌐 Web Version (Flask / FastAPI)

👩‍💻 Author

👤 Priya Thakur
🔗 GitHub: https://github.com/Priya-1800

🔗 LinkedIn: https://www.linkedin.com/in/priya-thakur-8701a1272/