#2025/11/15 ECPS205 Final Project... KEVIN_LEE
from picamera2 import Picamera2, Preview
import time as time

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
            self.picam.start_preview(Preview.QTGL)
            self.picam.start()
            time.sleep(1)
            self.preview = True
            print("Start preview\n")
            
    def stop_preview(self):
        
        if self.preview:
            self.picam.stop_preview()
            self.preview = False
            print("Stop preview\n")
            
    def take_shot(self):
        
        self.start_preview()
        take = input(r"[S] to take a shot >o<...[Q] to end App...")
        take = take.lower()
        if(take == "s"):
            self.picam.capture_file(f"cam0_{self.imgid}.jpg")
            print("An image taken...",f"cam0_{self.imgid}.jpg")
            self.imgid +=1
        else:
            print("No image taken...")
            
        return take
