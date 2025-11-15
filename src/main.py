#2025/11/15 ECPS205 Final Project... KEVIN_LEE

from cam import CameraController
import time as time

def main():
    print("=== Camera Controller ===")
    
    cam0 = CameraController(0, False)
    cam0.start_preview()
    
    while True:
        
        cmd = cam0.take_shot()
        
        if cmd == "q":
            break
    
    print("Stopping camera application....")
    time.sleep(2)
    cam0.stop_preview()


if __name__ == "__main__":
    main()
