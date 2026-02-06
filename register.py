import customtkinter as ctk
import bcrypt
import json
import os
import tkinter.messagebox as mb

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("400x420")
app.title("Register - Smart Attendance")

def register_user():
    username = user_entry.get()
    password = pass_entry.get()
    role = role_var.get()

    if not username or not password:
        mb.showerror("Error", "All fields required")
        return

    with open("users_db.json", "r") as f:
        users = json.load(f)

    if username in users:
        mb.showerror("Error", "User already exists")
        return

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    users[username] = {"password": hashed, "role": role}

    with open("users_db.json", "w") as f:
        json.dump(users, f, indent=4)

    os.makedirs(f"users/{username}", exist_ok=True)

    mb.showinfo("Success", "Registration successful!")
    app.destroy()
    os.system("python login.py")

ctk.CTkLabel(app, text="Register", font=("Segoe UI", 22, "bold")).pack(pady=20)

user_entry = ctk.CTkEntry(app, placeholder_text="Username")
user_entry.pack(pady=10)

pass_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*")
pass_entry.pack(pady=10)

role_var = ctk.StringVar(value="Teacher")
ctk.CTkOptionMenu(app, values=["Teacher","Staff","HOD"], variable=role_var).pack(pady=10)

ctk.CTkButton(app, text="Register", command=register_user).pack(pady=20)

app.mainloop()
