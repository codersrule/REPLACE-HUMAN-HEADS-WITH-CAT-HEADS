import cv2 as cv
import numpy as np

address = [
    "cat.png",
]

img = cv.imread(address[0], cv.IMREAD_UNCHANGED)

def make_cat(img, number): 
    """
    Extract a specific cat face from the sprite sheet
    """
    h = 997
    w = 1000
    y = [0, int(h/4-60), int(h/2-60), int(3*h/4-80), int(h-80)] 
    x = [0, int(w/4), int(w/2), int(3*w/4), int(w)] 

    i = number // 4
    j = number % 4

    smaller_img = img[y[j]:y[j+1], x[i]:x[i+1], :]

    return smaller_img

def remove_white_bg(img):
    """
    Remove white background from cat image and make it transparent
    """
    # Force BGR
    if img.shape[2] == 4:
        bgr = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
    else:
        bgr = img.copy()

    # Convert to HSV
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)

    # White = high brightness, very low saturation
    mask = (s < 25) & (v > 180)

    # Add alpha channel
    rgba = cv.cvtColor(bgr, cv.COLOR_BGR2BGRA)

    # Make white transparent
    rgba[mask] = (0, 0, 0, 0)

    return rgba


def cat_paste(bg, fg, x, y):
    """
    Paste a cat head with alpha blending onto background
    """
    h, w = fg.shape[:2]

    # Boundary safety
    if x + w > bg.shape[1] or y + h > bg.shape[0]:
        return bg
    
    # Also check for negative coordinates
    if x < 0 or y < 0:
        return bg

    b, g, r, a = cv.split(fg)
    alpha = a / 255.0

    for c in range(3):
        bg[y:y+h, x:x+w, c] = (
            alpha * fg[:, :, c] +
            (1 - alpha) * bg[y:y+h, x:x+w, c]
        )
    return bg


def load_all_cats(sprite_path):
    """
    Load all 16 cat faces from the sprite sheet
    """
    sprite = cv.imread(sprite_path, cv.IMREAD_UNCHANGED)
    if sprite is None:
        raise ValueError(f"Could not load sprite from {sprite_path}")
    
    cat_faces = []
    for i in range(16):
        cat = make_cat(sprite, i)
        cat = remove_white_bg(cat)
        cat_faces.append(cat)
    
    return cat_faces

