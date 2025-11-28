#2025/11/15 ECPS205 Final Project... KEVIN_LEE

from cam import CameraController
from cat import load_all_cats
from face_detection import FaceDetector
from head_swap import HeadSwapper
import cv2 as cv
import time
import os


# Output directory for saved images
OUTPUT_DIR = "outputs"


def create_output_dir():
    """Create outputs directory if it doesn't exist"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")


def main():
    # Create output directory
    create_output_dir()
    
    print("\nInitializing components...")
    
    # Initialize camera
    print("\n1. Starting camera...")
    cam0 = CameraController(0, False)
    cam0.start_preview()
    
    # Load cat faces
    print("\n2. Loading cat sprites...")
    try:
        cat_faces = load_all_cats("cat.png")
        print(f"Loaded {len(cat_faces)} cat faces")
    except Exception as e:
        print(f"Error loading cats: {e}")
        cam0.stop_preview()
        return
    
    # Initialize face detector
    print("\n3. Initializing face detector...")
    try:
        face_detector = FaceDetector()
    except Exception as e:
        print(f" Error initializing face detector: {e}")
        cam0.stop_preview()
        return
    
    # Initialize head swapper
    print("\n4. Initializing head swapper...")
    head_swapper = HeadSwapper(cat_faces, scale_factor=1.3)
    
    print("\n" + "-"*60)
    print("LIVE TRACKING WINDOW - Press keys for controls:")
    print("  [Q] - Quit")
    print("  [S] - Save screenshot")
    print("  [C] - Change cat set")
    print("  [+] - Increase cat size")
    print("  [-] - Decrease cat size")
    print("  [D] - Toggle debug mode (show face boxes)")
    print("-"*60 + "\n")
    
    # Stats
    frame_count = 0
    start_time = time.time()
    screenshot_count = 0
    debug_mode = False
    
    # Create window with properties
    window_name = "Cat Head Swap - Live Tracking"
    cv.namedWindow(window_name, cv.WINDOW_NORMAL)
    cv.resizeWindow(window_name, 720, 720)
    
    try:
        while True:
            # Capture frame from camera
            frame = cam0.capture_frame()
            
            # Convert RGB to BGR for OpenCV
            frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
            
            # Detect faces
            faces = face_detector.detect_faces(
                frame,
                scale_factor=1.1,
                min_neighbors=5,
                min_size=(50, 50)
            )
            
            # Debug mode: show face boxes BEFORE swapping
            if debug_mode:
                # Draw boxes in red to show original detection
                for (x, y, w, h) in faces:
                    cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    # Draw center point
                    center_x = x + w // 2
                    center_y = y + h // 2
                    cv.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            
            # Swap heads with cats
            frame = head_swapper.swap_heads(frame, faces)
            
            # Calculate FPS
            frame_count += 1
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            
            # Create info panel at top of frame
            info_height = 180
            info_panel = frame[0:info_height, :].copy()
            # Semi-transparent overlay
            overlay = info_panel.copy()
            cv.rectangle(overlay, (0, 0), (frame.shape[1], info_height), (0, 0, 0), -1)
            cv.addWeighted(overlay, 0.6, info_panel, 0.4, 0, info_panel)
            frame[0:info_height, :] = info_panel
            
            # Display info with better formatting
            cv.putText(frame, f"Faces Detected: {len(faces)}", (10, 75),
                      cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            cv.putText(frame, f"Cat Set: {head_swapper.current_cat_set}", (10, 115),
                      cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            cv.putText(frame, f"Scale: {head_swapper.scale_factor:.1f}x", (10, 155),
                      cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            
            if debug_mode:
                cv.putText(frame, "DEBUG MODE - RED BOXES", (400, 35),
                          cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            
            # Show live tracking window
            cv.imshow(window_name, frame)
            
            # Handle key presses
            key = cv.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\nQuitting...")
                break
            
            elif key == ord('s'):
                filename = os.path.join(OUTPUT_DIR, f"headswap_{screenshot_count:03d}.jpg")
                cv.imwrite(filename, frame)
                print(f" Screenshot saved: {filename}")
                screenshot_count += 1
            
            elif key == ord('c'):
                cat_set = head_swapper.change_cat_set()
                print(f"Changed to cat set: {cat_set}")
            
            elif key == ord('+') or key == ord('='):
                new_scale = head_swapper.scale_factor + 0.1
                head_swapper.set_scale_factor(new_scale)
            
            elif key == ord('-') or key == ord('_'):
                new_scale = head_swapper.scale_factor - 0.1
                head_swapper.set_scale_factor(new_scale)
            
            elif key == ord('d'):
                debug_mode = not debug_mode
                print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")
    
    except KeyboardInterrupt:
        print("\nInterrupted by user...")
    
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup and summary
        print("\n" + "-"*60)
        print("SUMMARY")
        print("-"*60)
        print(f"Screenshots saved: {screenshot_count}")

        if screenshot_count > 0:
            print(f"Output folder: {OUTPUT_DIR}/")
        print("-"*60 + "\n")
        
        print("Stopping camera...")
        time.sleep(1)
        cam0.stop_preview()
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()
