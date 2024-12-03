import pyautogui
import zlib
from PIL import Image
import numpy as np
import cv2

def capture_screen(resolution=(1200, 680)):
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.resize(resolution)
    return zlib.compress(screenshot.tobytes())

def decompress_screen(data, resolution=(1200, 675)):
    try:
        img_data = zlib.decompress(data)
        image = Image.frombytes('RGB', resolution, img_data)
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise ValueError(f"Failed to decompress or reconstruct image: {e}")