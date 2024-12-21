import tkinter as tk
from datetime import datetime
from threading import Thread
import time
import simpleaudio as sa
import os

def play_sound(file_path):
    try:
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        print(f"Error playing sound: {e}")

def update_countdown_label(label):
    while True:
        now = datetime.now()
        update_status_label(now)
        if now.minute < 15:
            target_minute = 15
        elif now.minute < 45:
            target_minute = 45
        else:
            target_minute = 60

        remaining_time = (target_minute * 60 - now.minute * 60 - now.second) % 3600
        minutes_left = remaining_time // 60
        seconds_left = remaining_time % 60
        label.config(text=f"{minutes_left:02}:{seconds_left:02}")
        time.sleep(1)

def update_status_label(now):
    if 0 <= now.minute < 15:
        text_label.config(text="다음 상선 대기중")
        countdown_label.config(fg="black")
    elif now.minute == 15 and now.second <= 34:
        text_label.config(text="상선 접근중")
        countdown_label.config(fg="#f0ad4e")
        if not hasattr(update_status_label, "last_state") or update_status_label.last_state != "approach":
            play_sound(os.path.join(os.path.dirname(__file__), "sfx/Merchant_Come.wav"))
            update_status_label.last_state = "approach"
    elif 15 < now.minute < 30 or (now.minute == 15 and now.second > 34):
        text_label.config(text="상선 유지중")
        countdown_label.config(fg="#0275d8")
        if not hasattr(update_status_label, "last_state") or update_status_label.last_state != "maintain":
            play_sound(os.path.join(os.path.dirname(__file__), "sfx/Merchant_Here.wav"))
            update_status_label.last_state = "maintain"
    elif 30 <= now.minute < 45:
        text_label.config(text="다음 상선 대기중")
        countdown_label.config(fg="black")
        update_status_label.last_state = "wait"
    elif now.minute == 45 and now.second <= 34:
        text_label.config(text="상선 접근중")
        countdown_label.config(fg="#f0ad4e")
        if not hasattr(update_status_label, "last_state") or update_status_label.last_state != "approach":
            play_sound(os.path.join(os.path.dirname(__file__), "sfx/Merchant_Come.wav"))
            update_status_label.last_state = "approach"
    elif 45 < now.minute < 60 or (now.minute == 45 and now.second > 34):
        text_label.config(text="상선 유지중")
        countdown_label.config(fg="#0275d8")
        if not hasattr(update_status_label, "last_state") or update_status_label.last_state != "maintain":
            play_sound(os.path.join(os.path.dirname(__file__), "sfx/Merchant_Here.wav"))
            update_status_label.last_state = "maintain"

# GUI Setup
root = tk.Tk()
root.title("Merchant Waiter")
root.geometry("280x110")

# Set Program Icon
icon_path = os.path.join(os.path.dirname(__file__), "Icon/Icon.ico")
root.iconbitmap(icon_path)

# Text Label
text_label = tk.Label(root, text="Status_Here", font=("Helvetica", 18))
text_label.pack(side="top", pady=4)

# Countdown Display Label
countdown_label = tk.Label(root, text="--:--", font=("Helvetica", 38))
countdown_label.pack(side="bottom", pady=6)

# Threads for Countdown Update and Beep Check
Thread(target=update_countdown_label, args=(countdown_label,), daemon=True).start()

# Start GUI Loop
root.mainloop()
