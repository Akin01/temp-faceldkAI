import cv2
from ai_detection import start_detection
from temp_data import data_ready
from temp_arduino import Arduino
import os


# port = os.getenv("PORT")
# bauderate = os.getenv("BAUDERATE")
# ard = Arduino(port, bauderate)


# def get_temp_data():
#     ser = ard.open_serial()
#     temp_data = ard.get_temp(ser)
#     ard.close_serial(ser)
#     return temp_data


if __name__ == '__main__':
    # Initialize camera
    cap = cv2.VideoCapture(0)

    # Start Face and Landmark detection
    start_detection(cap, "Temperature Face Detection ")