import cv2
from src.ai_detection import start_detection

if __name__ == '__main__':
    # Initialize camera
    cap = cv2.VideoCapture(0)

    # Start Face and Landmark detection
    start_detection(cap, "Temperature Face Detection")
