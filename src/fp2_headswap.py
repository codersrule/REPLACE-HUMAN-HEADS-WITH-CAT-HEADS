# https://github.com/codersrule/REPLACE-HUMAN-HEADS-WITH-CAT-HEADS.git
import os
import time
import threading
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from PIL import Image, ImageTk
# ---------- Configuration ----------
SAVE_PATH = "/home/raoab/src/ecps205-fp2/tvi"
IMAGE_PATH = os.path.join(SAVE_PATH, "images")
VIDEO_PATH = os.path.join(SAVE_PATH, "videos")
# Ensure directories exist
os.makedirs(IMAGE_PATH, exist_ok=True)
os.makedirs(VIDEO_PATH, exist_ok=True)
# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration()) # Default to still image mode
# ---------- Tkinter GUI ----------
root = tk.Tk()
root.title("Head Swap!")
root.resizable(False, False)
WINDOW_WIDTH = 1200
root.geometry(f"{WINDOW_WIDTH}x100")
style=ttk.Style(root)
style.theme_use('clam')
video_window = None
recording = False
encoder = None
video_filename = ""
countdown_label = None  
image_label = None      

# ---------- Helper Functions ----------
def get_timestamp():
# """Returns a timestamp string.""" 
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# ---------- Video Window Handling ----------
def create_video_window():
    """Creates the video feed window when preview starts."""
    global video_window, countdown_label
    if video_window is None or not video_window.winfo_exists():
        video_window = tk.Toplevel(root)
        video_window.title("Live Head Swap! Cam")
        video_window.protocol("WM_DELETE_WINDOW", stop_preview)
        video_window.geometry("650x550") # Increased height for countdown padding
    global image_label
    image_label = tk.Label(video_window)
    image_label.pack()
    # Countdown Label (Positioned Below Video)
    countdown_label = tk.Label(video_window, text="", font=("Arial", 30, "bold"), fg="red")
    countdown_label.pack(pady=20) # Adds padding below video feed

def update_preview():
    """Continuously updates the Tkinter Label with live preview frames."""
    if video_window is None or not video_window.winfo_exists():
        return
    frame = picam2.capture_array()
    img = Image.fromarray(frame).resize((640, 480))
    tk_img = ImageTk.PhotoImage(img)
    image_label.config(image=tk_img)
    image_label.image = tk_img
    video_window.after(50, update_preview)

def start_preview():
    """Starts live preview and opens video feed window."""
    create_video_window()
    try:
        picam2.start()
        update_preview()
    except Exception as e:
        print(f"Error starting preview: {e}")

def stop_preview():
    """Stops live preview and closes video feed window."""
    try:
        if video_window:
            video_window.destroy()
            picam2.stop()
    except Exception as e:
        print(f"Error stopping preview: {e}")

# ---------- Capture Image ----------
def capture_image():
    """Captures an image and saves it without freezing."""
    def _capture():
        filename = os.path.join(IMAGE_PATH, f"img_{get_timestamp()}.jpg")
        try:
            print("Capturing image...")
            img = picam2.capture_image()
            img = img.convert("RGB")
            img.save(filename)
            print(f"Image saved: {filename}")
        except Exception as e:
            print(f"Error capturing image: {e}")
    threading.Thread(target=_capture, daemon=True).start()

# ---------- Countdown Timer Below Video ----------
def start_recording():
    """Starts the countdown timer before recording."""
    print("DEBUG: start_recording() called")  
    # Make sure preview is running first
    if video_window is None or not video_window.winfo_exists():
        print("Please start camera first before recording!")
        # Optionally show a popup
        messagebox.showerror("Error", "start Camera first!")
        return
    
    if countdown_label is None:
        print("ERROR: Countdown label not initialized!")
        return
    show_countdown_timer(3)

def show_countdown_timer(count):
    """Updates the countdown timer below the video feed."""
    print(f"DEBUG: show_countdown_timer called with count={count}")
    
    # Debug each condition
    print(f"DEBUG: video_window is None? {video_window is None}")
    if video_window is not None:
        print(f"DEBUG: video_window.winfo_exists()? {video_window.winfo_exists()}")
    print(f"DEBUG: countdown_label is None? {countdown_label is None}")
    if countdown_label is not None:
        try:
            print(f"DEBUG: countdown_label.winfo_exists()? {countdown_label.winfo_exists()}")
        except:
            print("DEBUG: countdown_label.winfo_exists() threw an error")
    
    try:
        if (video_window is not None and video_window.winfo_exists() and
            countdown_label is not None and countdown_label.winfo_exists()):
            print(f"DEBUG: Setting countdown to {count}")
            countdown_label.config(text=str(count))
            if count > 0:
                video_window.after(1000, show_countdown_timer, count - 1)
            else:
                countdown_label.config(text="")
                print("DEBUG: Calling start_recording_after_countdown")
                start_recording_after_countdown()
        else:
            print("DEBUG: Condition check FAILED - countdown not displayed")
    except tk.TclError as e:
        print(f"DEBUG: TclError in countdown: {e}")
    except Exception as e:
        print(f"DEBUG: Unexpected countdown error: {e}")

def start_recording_after_countdown():
    """Starts recording video after countdown finishes."""
    print("DEBUG: start_recording_after_countdown() called")  # ✅ Add this
    global recording, encoder, video_filename
    if recording:
        print("Already recording...")
        return
    
    video_filename = os.path.join(VIDEO_PATH, f"video_{get_timestamp()}.h264")
    encoder = H264Encoder()
    try:
        print(f"Recording video: {video_filename}")
        recording = True
        picam2.stop()
        picam2.configure(picam2.create_video_configuration())
        picam2.start()
        picam2.start_recording(encoder, video_filename)
        print("DEBUG: Recording started successfully")  # ✅ Add this
    except Exception as e:
        print(f"Error starting recording: {e}")

# ---------- Stop Recording & Convert to MP4 ----------
def stop_recording():
    """Stops recording and converts to MP4 without freezing."""
    global recording, encoder, video_filename
    if not recording:
        print("Not currently recording...")
        return  # ✅ Only return if not recording
    
    def _stop():  # ✅ Nested function inside stop_recording
        global recording, encoder, video_filename
        try:
            print("Stopping recording...")
            picam2.stop_recording()
            picam2.stop()
            picam2.configure(picam2.create_still_configuration())
            picam2.start()
            recording = False
            encoder = None
            
            if video_filename:
                mp4_filename = video_filename.replace(".h264", ".mp4")
                
                def convert_to_mp4():  # ✅ Nested inside _stop
                    try:
                        print(f"Converting {video_filename} to {mp4_filename}...")
                        subprocess.run(["ffmpeg", "-i", video_filename, "-c:v", "copy", 
                                      "-movflags", "+faststart", mp4_filename], check=True)
                        os.remove(video_filename)
                        print(f"Conversion complete! Saved as: {mp4_filename}")
                    except Exception as e:
                        print(f"Error converting video: {e}")
                
                threading.Thread(target=convert_to_mp4, daemon=True).start()  # ✅ Inside _stop
        except Exception as e:
            print(f"Error stopping recording: {e}")
    
    threading.Thread(target=_stop, daemon=True).start()  # ✅ Inside stop_recording, calls _stop

def select_cat_faces():
    """Launches the cat face selection script."""
    try:
        messagebox.showerror("Error", "cat face selection not implemented!")
    except Exception as e:
        print(f"Error launching cat face selection: {e}")
        
def hs_settings():
    """Launches the Head Swap! settings script."""
    try:
        messagebox.showerror("Error", "hs_settings not implemented!")
    except Exception as e:
        print(f"Error launching Head Swap! settings: {e}")
        
def start_head_swap():
    """Starts the Head Swap! process."""
    try:
        messagebox.showerror("Error", "start_head_swap not implemented!")
    except Exception as e:
        print(f"Error starting Head Swap!: {e}")

def stop_head_swap():
    """Stops the Head Swap! process."""
    try:
        messagebox.showerror("Error", "stop_head_swap not implemented!")
    except Exception as e:
        print(f"Error stopping Head Swap!: {e}")
        
# ---------- Tkinter Buttons ----------
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)
start_preview_button = tk.Button(buttons_frame, text="Start Camera", width=18, command=start_preview)
start_preview_button.grid(row=0, column=0, padx=5)
stop_preview_button = tk.Button(buttons_frame, text="Stop Camera", width=18, command=stop_preview)
stop_preview_button.grid(row=0, column=1, padx=5)
capture_button = tk.Button(buttons_frame, text="Take a Picture", width=18, command=capture_image)
capture_button.grid(row=0, column=2, padx=5)
start_video_button = tk.Button(buttons_frame, text="Start Cam Recording", width=18, command=start_recording)
start_video_button.grid(row=0, column=3, padx=5)
stop_video_button = tk.Button(buttons_frame, text="Stop Cam Recording", width=18, command=stop_recording)
stop_video_button.grid(row=0, column=4, padx=5)
select_cat_faces_button = tk.Button(buttons_frame, text="Select Cat Faces", width=18, command=select_cat_faces)
select_cat_faces_button.grid(row=1, column=0, padx=5)

try:
    icon_image = Image.open("/home/raoab/src/ecps205-fp2/tvi/cat_icon.png")  
    icon_image = icon_image.resize((40, 40))  # Resize to 40x40 pixels
    icon_photo = ImageTk.PhotoImage(icon_image)
    
    icon_label = tk.Label(buttons_frame, image=icon_photo)
    icon_label.image = icon_photo  # Keep a reference to prevent garbage collection
    icon_label.grid(row=1, column=2, pady=5)  # Row 1, same column as capture button
except Exception as ex:
    print(f"Could not load icon: {ex}")

hs_settings_button = tk.Button(buttons_frame, text="Head Swap! Settings", width=18, command=hs_settings)
hs_settings_button.grid(row=1, column=1, padx=5)
start_head_swap_button = tk.Button(buttons_frame, text="Start Head Swap!", width=18, command=start_head_swap)
start_head_swap_button.grid(row=1, column=3, padx=5)
stop_head_swap_button = tk.Button(buttons_frame, text="Stop Head Swap!", width=18, command=stop_head_swap)
stop_head_swap_button.grid(row=1, column=4, padx=5)


# Quit button to exit safely
def on_closing():
    """Ensures clean shutdown of camera before exiting."""
    stop_preview()
    root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)

# Start Tkinter main loop
root.mainloop()
