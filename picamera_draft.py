import picamera
import io
import time
from PIL import Image, ImageEnhance
import pytessaract
import numpy as np
import cv2

class Camera:
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1024, 768)
        time.sleep(2)

    def capture_image(self):
        buffer = io.BytesIO()
        self.camera.capture(buffer, format='jpeg')
        buffer.seek(0)
        image = Image.open(buffer)
        return image
    
    def preprocess_image(self, image):
        image = image.convert('L')
        image = ImageEnhance.Contrast(image).enhance(2.0)
        image_cv = np.array(image)

        image_cv = cv2.adaptiveThreshold(
            image_cv, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 31, 2
        )
        image_cv = cv2.resize(image_cv, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        return Image.fromarray(image_cv)

    
if __name__ == "__main__":
    cam = Camera()
    
    while True:
        img = cam.capture_image()
        print("Captured image!")
        img_proc = cam.preprocess_image(img)

        text = pytessaract.image_to_string(img_proc)
        print("Extracted Text:")
        print(text.strip())
        print("-" * 40)

        time.sleep(1)