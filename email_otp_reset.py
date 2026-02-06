import customtkinter as ctk
import json, random, bcrypt, yagmail, tkinter.messagebox as mb

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("420x460")
app.title("Reset Password (OTP)")

OTP = None
USER = None

def send_otp():
    global OTP, USER
    username = user_entry.get()
    email = email_entry.get()

    with open("users_db.json","r") as f:
        users = json.load(f)

    if username not in users or users[username]["email"] != email:
        mb.showerror("Error","Invalid username or email")
        return

    OTP = str(random.randint(100000,999999))
    USER = username

    sender = yagmail.SMTP("yourgmail@gmail.com","APP_PASSWORD_HERE")
    sender.send(to=email, subject="Your OTP - Smart Attendance", contents=f"Your OTP is: {OTP}")

    mb.showinfo("OTP Sent","OTP sent to your email")
    otp_entry.configure(state="normal")
    newpass_entry.configure(state="normal")
    reset_btn.configure(state="normal")

def reset_password():
    user_otp = otp_entry.get()
    new_pass = newpass_entry.get()

    if user_otp != OTP:
        mb.showerror("Error","Invalid OTP")
        return

    with open("users_db.json","r") as f:
        users = json.load(f)

    hashed = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt()).decode()
    users[USER]["password"] = hashed

    with open("users_db.json","w") as f:
        json.dump(users,f,indent=4)

    mb.showinfo("Success","Password reset successful!")
    app.destroy()

ctk.CTkLabel(app,text="Email OTP Password Reset",font=("Segoe UI",20,"bold")).pack(pady=15)

user_entry = ctk.CTkEntry(app, placeholder_text="Username")
user_entry.pack(pady=8)

email_entry = ctk.CTkEntry(app, placeholder_text="Registered Email")
email_entry.pack(pady=8)

ctk.CTkButton(app,text="📧 Send OTP",command=send_otp).pack(pady=10)

otp_entry = ctk.CTkEntry(app, placeholder_text="Enter OTP", state="disabled")
otp_entry.pack(pady=8)

newpass_entry = ctk.CTkEntry(app, placeholder_text="New Password", show="*", state="disabled")
newpass_entry.pack(pady=8)

reset_btn = ctk.CTkButton(app,text="🔁 Reset Password",command=reset_password,state="disabled")
reset_btn.pack(pady=15)

app.mainloop()
