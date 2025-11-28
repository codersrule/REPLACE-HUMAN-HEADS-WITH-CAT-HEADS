
import cv2 as cv
import numpy as np
import os


class FaceDetector:
    def __init__(self, cascade_path=None):
        """
        Initialize face detector
        """
        if cascade_path is None:
            # Try multiple common locations for the cascade file
            cascade_path = self._find_cascade_file()
        
        self.face_cascade = cv.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            raise ValueError(f"Could not load cascade classifier from {cascade_path}")
        
        print(f"Face detector initialized using: {cascade_path}")
    
    def _find_cascade_file(self):
        """
        Try to find the Haar Cascade XML file in common locations
        I added all the possible paths because they are very unreliable
        """
        # List of possible locations
        possible_paths = [
            # Try OpenCV's data directory (newer versions)
            '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml',
            
            # Older OpenCV versions
            '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml',
            '/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml',
            '/usr/local/share/opencv/haarcascades/haarcascade_frontalface_default.xml',
            
            # Current directory (if user downloaded it)
            'haarcascade_frontalface_default.xml',
            './haarcascade_frontalface_default.xml',
            
            # Home directory
            os.path.expanduser('~/haarcascade_frontalface_default.xml'),
        ]
        
        # Try to use cv2.data if available (Python package installations)
        try:
            data_path = cv.data.haarcascades + 'haarcascade_frontalface_default.xml'
            possible_paths.insert(0, data_path)
        except AttributeError:
            pass  # cv2.data not available
        
        # Try each path
        for path in possible_paths:
            if os.path.exists(path):
                print(f"Found cascade file at: {path}")
                return path
        
        # If nothing found, provide helpful error message
        error_msg = (
            "Could not find haarcascade_frontalface_default.xml\n"
            "Please download it from:\n"
            "https://github.com/opencv/opencv/raw/master/data/haarcascades/haarcascade_frontalface_default.xml\n"
            "And place it in the same directory as this script.\n\n"
            "Or install it with:\n"
            "sudo apt-get install opencv-data\n\n"
            "Tried these locations:\n" + "\n".join(possible_paths)
        )
        raise FileNotFoundError(error_msg)
    
    def detect_faces(self, frame, scale_factor=1.1, min_neighbors=5, min_size=(50, 50)):
        """
        Detect faces in a frame
        
        Returns:
            Array of face rectangles [(x, y, w, h), ...]
        """
        # Convert to grayscale for detection
        if len(frame.shape) == 3:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        else:
            gray = frame
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=min_size,
            flags=cv.CASCADE_SCALE_IMAGE
        )
        
        return faces
    
    def draw_face_boxes(self, frame, faces, color=(0, 255, 0), thickness=2):
        """
        Draw rectangles around detected faces (for debugging)
        
        Returns:
            Frame with boxes drawn
        """
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x+w, y+h), color, thickness)
        
        return frame
    
    def get_face_centers(self, faces):
        """
        Calculate center points of detected faces
            
        Returns:
            List of (center_x, center_y) tuples
        """
        centers = []
        for (x, y, w, h) in faces:
            center_x = x + w // 2
            center_y = y + h // 2
            centers.append((center_x, center_y))
        
        return centers
    
    def get_largest_face(self, faces):
        """
        Get the largest detected face
            
        Returns:
            Tuple (x, y, w, h) of largest face, or None if no faces
        """
        if len(faces) == 0:
            return None
        
        # Find face with largest area
        largest = max(faces, key=lambda f: f[2] * f[3])
        return tuple(largest)
