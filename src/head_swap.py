
import cv2 as cv
import numpy as np
from cat import cat_paste


class HeadSwapper:
    def __init__(self, cat_faces, scale_factor=1.3):
        """
        Initialize head swapper
        """
        self.cat_faces = cat_faces
        self.scale_factor = scale_factor # We scale the sprite to match human face
        self.current_cat_set = 0
        
        print(f"HeadSwapper initialized with {len(cat_faces)} cat faces")
    
    def swap_heads(self, frame, faces):
        """
        Replace detected faces with cat heads
        """
        for idx, (x, y, w, h) in enumerate(faces):
            # Select which cat to use
            cat_idx = (idx + self.current_cat_set) % len(self.cat_faces)
            cat = self.cat_faces[cat_idx]
            
            # Calculate new size with scale factor
            new_w = int(w * self.scale_factor)
            new_h = int(h * self.scale_factor)
            
            # Resize cat to fit the face
            cat_resized = cv.resize(cat, (new_w, new_h), interpolation=cv.INTER_AREA)
            
            # Center the cat over the detected face
            offset_x = x - (new_w - w) // 2
            offset_y = y - (new_h - h) // 2
            
            # Paste the cat head with transparency
            frame = cat_paste(frame, cat_resized, offset_x, offset_y)
        
        return frame
    
    def swap_heads_custom(self, frame, faces, cat_indices=None):
        """
        Replace faces with specific cat selections
        """
        for idx, (x, y, w, h) in enumerate(faces):
            # Select cat
            if cat_indices and idx < len(cat_indices):
                cat_idx = cat_indices[idx] % len(self.cat_faces)
            else:
                cat_idx = (idx + self.current_cat_set) % len(self.cat_faces)
            
            cat = self.cat_faces[cat_idx]
            
            # Calculate new size
            new_w = int(w * self.scale_factor)
            new_h = int(h * self.scale_factor)
            
            # Resize cat
            cat_resized = cv.resize(cat, (new_w, new_h), interpolation=cv.INTER_AREA)
            
            # Center placement
            offset_x = x - (new_w - w) // 2
            offset_y = y - (new_h - h) // 2
            
            # Paste cat
            frame = cat_paste(frame, cat_resized, offset_x, offset_y)
        
        return frame
    
    def change_cat_set(self):
        """Cycle to next cat set"""
        self.current_cat_set = (self.current_cat_set + 1) % len(self.cat_faces)
        return self.current_cat_set
    
    def set_scale_factor(self, scale):
        
        if 0.5 <= scale <= 3.0:
            self.scale_factor = scale
            print(f"Scale factor set to {scale}")
        else:
            print(f"Warning: Scale {scale} out of range (0.5-3.0)")
