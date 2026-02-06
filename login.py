import customtkinter as ctk
import bcrypt
import json
import os
import tkinter.messagebox as mb

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("400x360")
app.title("Login - Smart Attendance")

def login_user():
    username = user_entry.get()
    password = pass_entry.get()

    with open("users_db.json", "r") as f:
        users = json.load(f)

    if username not in users:
        mb.showerror("Error", "User not found")
        return

    stored_hash = users[username]["password"].encode()

    if bcrypt.checkpw(password.encode(), stored_hash):
        mb.showinfo("Success", f"Welcome {username}")
        os.environ["LOGGED_USER"] = username
        app.destroy()
        os.system("python ui_app.py")
    else:
        mb.showerror("Error", "Wrong password")

ctk.CTkLabel(app, text="Login", font=("Segoe UI", 22, "bold")).pack(pady=20)

user_entry = ctk.CTkEntry(app, placeholder_text="Username")
user_entry.pack(pady=10)

pass_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*")
pass_entry.pack(pady=10)

ctk.CTkButton(app, text="Login", command=login_user).pack(pady=20)

ctk.CTkButton(app, text="Go to Register", command=lambda: os.system("python register.py")).pack(pady=10)

ctk.CTkButton(app, text="Forgot Password (Email OTP)", 
    command=lambda: os.system("python email_otp_reset.py")
).pack(pady=8)

app.mainloop()

