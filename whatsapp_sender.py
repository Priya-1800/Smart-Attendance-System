import pywhatkit as kit
import pyautogui
import time
def send_whatsapp_message(phone_number, message):
    try:
        # Increased wait_time to give WhatsApp Web more time to load
        kit.sendwhatmsg_instantly(phone_number, message, wait_time=25, tab_close=True, close_time=15)
        
        # Increased sleep duration to ensure the typing area is active
        time.sleep(10)
        
        # Press Enter to send the message
        pyautogui.press('enter')
        
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    send_whatsapp_message("+917410597912", "Hello from attendance system!")