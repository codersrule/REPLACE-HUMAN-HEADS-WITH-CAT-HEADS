#2025/11/15 ECPS205 Final Project... KEVIN_LEE
from picamera2 import Picamera2, Preview
import time as time
import os

class CameraController:
    def __init__(self, camid = 0, preview = False):
        """Init Camera"""
        self.camid = camid
        self.picam = Picamera2(camid)
        self.preview = preview
        self.imgid = 0
        print("Camera Init\n")

    def start_preview(self):

        if not self.preview:
            # Try different preview modes based on environment
            display = os.environ.get('DISPLAY', '')

            try:
                if display and 'localhost' in display:
                    # Remote X11 - use QT
                    print("Using QT preview for X11 forwarding...")
                    self.picam.start_preview(Preview.QT)
                elif display:
                    # Local display - try QTGL first
                    print("Using QTGL preview...")
                    self.picam.start_preview(Preview.QTGL)
                else:
                    # No display - run headless
                    print("No display detected, running headless...")
            except Exception as e:
                print(f"Preview failed: {e}")
                print("Running in headless mode...")

            self.picam.start()
            time.sleep(1)
            self.preview = True
            print("Camera started\n")

    def stop_preview(self):

        if self.preview:
            try:
                self.picam.stop_preview()
            except:
                pass
            self.picam.stop()
            self.preview = False
            print("Camera stopped\n")

    def take_shot(self):

        self.start_preview()
        take = input(r"[S] to take a shot >o<...[Q] to end App...")
        take = take.lower()
        if(take == "s"):
            self.picam.capture_file(f"cam0_{self.imgid}.jpg")
            print("Image captured:",f"cam0_{self.imgid}.jpg")
            self.imgid +=1
        elif take == "q":
            print("Exiting application...")
        else:
            print("No image taken...")

        return take