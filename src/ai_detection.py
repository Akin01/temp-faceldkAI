import cv2
import mediapipe as mp

from dotenv import load_dotenv
import os
import time

from draw import Draw
import draw
from temp_data import post_data, data_ready
from arduino_uno import Arduino

load_dotenv()

# Arduino configuration
port = os.getenv("PORT")
bauderate = os.getenv("BAUDERATE")

# Use Method for face detection from mediapipe
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection()

# Use Method for landmark detection from mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Use Method utility for draw filter
mp_drawing = mp.solutions.drawing_utils


def get_temp_data():
    ard = Arduino(port, bauderate)
    temp_data = ard.get_temp("#")
    ard.close_serial()
    return temp_data


def start_detection(cap, window_title: str = None):
    # Time Initialization for calculate FPS
    previous_time = 0

    while cap.isOpened():
        success, image = cap.read()

        h, w, c = image.shape

        image = cv2.flip(image, 1)

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Activate writeable and rgb -> bgr
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Face Detections using mediapipe solution
        face_results = face_detection.process(image)

        # Hand Landmark Detection using mediapipe solution
        ldk_result = hands.process(image)

        # Deactivate writeable and bgr -> rgb
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Initialize draw library
        d = Draw(image)

        if face_results.detections:
            temp_alert = "Data not found" if get_temp_data() else get_temp_data()

            # Body temperature box
            d.Rect((-210, -160), (-100, -90), draw.COLOR_NAVY, draw.THICK_WEIGHT_FILLED)
            d.Rect((-210, -210), (-100, -160), draw.COLOR_BLACK, draw.THICK_WEIGHT_FILLED)

            # Body temperature title box
            d.Text("Suhu Tubuh",
                   -200,
                   -180,
                   draw.SERIF_SMALL,
                   draw.TEXT_SIZE_SMALL - 0.15,
                   draw.TEXT_WEIGHT_REGULAR,
                   draw.COLOR_WHITE)

            # Body temperature data in realtime display
            d.Text(f"{temp_alert[0]}  C",
                   -200,
                   -120,
                   draw.SANS_SERIF_NORMAL,
                   draw.TEXT_SIZE_SMALL,
                   draw.TEXT_WEIGHT_MEDIUM,
                   draw.COLOR_WHITE)

            # Body temperature degree symbol
            d.Circle(-135, -135, 3, draw.COLOR_WHITE, draw.THICK_WEIGHT_MEDIUM)

            # Environment temperature box
            d.Rect((-210, -10), (-100, 60), draw.COLOR_NAVY, draw.THICK_WEIGHT_FILLED)
            d.Rect((-210, -60), (-100, -10), draw.COLOR_BLACK, draw.THICK_WEIGHT_FILLED)

            # Environment temperature title box
            d.Text("Suhu Lingk.",
                   -200,
                   -30,
                   draw.SERIF_SMALL,
                   draw.TEXT_SIZE_SMALL - 0.15,
                   draw.TEXT_WEIGHT_REGULAR,
                   draw.COLOR_WHITE)

            # Environment temperature data in realtime display
            d.Text(f"{temp_alert[1]}  C",
                   -200,
                   30,
                   draw.SANS_SERIF_NORMAL,
                   draw.TEXT_SIZE_SMALL,
                   draw.TEXT_WEIGHT_MEDIUM,
                   draw.COLOR_WHITE)

            # Environment temperature degree symbol
            d.Circle(-135, 15, 3, draw.COLOR_WHITE, draw.THICK_WEIGHT_MEDIUM)

            # Face detected alert box
            d.Rect((190, -295), (365, -260), draw.COLOR_BLACK, draw.THICK_WEIGHT_FILLED)
            d.Rect((190, -295), (365, -260), draw.COLOR_DARK_SLATE_GRAY, draw.THICK_WEIGHT_REGULAR)

            # Face detected alert display
            d.Text("Face Detected",
                   200,
                   -270,
                   draw.SANS_SERIF_NORMAL,
                   draw.TEXT_SIZE_SMALL,
                   draw.TEXT_WEIGHT_REGULAR,
                   draw.COLOR_WHITE)

            for detection in face_results.detections:
                mp_drawing.draw_detection(image, detection)

        # Draw the Hand Landmark detection on the image.
        if ldk_result.multi_hand_landmarks:
            for hand_ldk in ldk_result.multi_hand_landmarks:
                for idx, dim in enumerate(hand_ldk.landmark):
                    xHand, yHand = int(dim.x * w), int(dim.y * h)

                    if (idx % 4 == 0) and (idx != 0):
                        d.Circle(xHand - int(h / 2), yHand - int(w / 2), 10, draw.COLOR_BLACK, draw.THICK_WEIGHT_BOLD)

                        if (518 > xHand > 460) and (405 > yHand > 350):
                            temp_body, temp_env = get_temp_data()
                            post_data_ready = data_ready(temp_body, temp_env)

                            res_post_status = post_data(post_data_ready)

                            if res_post_status.status_code == 201:
                                d.Text("Data has recorded",
                                       -100,
                                       100,
                                       draw.SANS_SERIF_SMALL,
                                       draw.TEXT_SIZE_NORMAL,
                                       draw.TEXT_WEIGHT_MEDIUM,
                                       draw.COLOR_YELLOW)

                mp_drawing.draw_landmarks(image, hand_ldk, mp_hands.HAND_CONNECTIONS)

        # Show fps on window
        current_time = time.time()
        fps = int(1 / (current_time - previous_time))

        previous_time = current_time

        # FPS value box
        d.Rect((-210, -300), (-100, -255), draw.COLOR_MIDNIGHT_BLUE, draw.THICK_WEIGHT_FILLED)
        d.Rect((-210, -300), (-100, -255), draw.COLOR_BLUE, draw.THICK_WEIGHT_REGULAR)

        fps_color = draw.COLOR_RED if fps < 20 else (draw.COLOR_YELLOW if fps < 35 else draw.COLOR_GREEN)

        # FPS value display in realtime
        d.Text(f"{fps} fps",
               -190,
               -270,
               draw.SANS_SERIF_NORMAL,
               draw.TEXT_SIZE_SMALL,
               draw.TEXT_WEIGHT_REGULAR,
               fps_color)

        # Show Video and set title
        cv2.imshow(window_title, image)

        if cv2.waitKey(5) == ord("q"):
            break

    cap.release()
