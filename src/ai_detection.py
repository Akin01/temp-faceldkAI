import cv2
import mediapipe as mp
import time
from draw import Draw
import draw
from post_temp import postTemp
from temp_data import data_ready

# Use Method for face detection from mediapipe
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection()

# Use Method for landmark detection from mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Use Method utility for draw filter
mp_drawing = mp.solutions.drawing_utils


def start_detection(cap, window_title: str = None, temp_data: float = None):
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
            temp_alert = "Data not found" if temp_data else temp_data

            d.Text(temp_alert,
                   50,
                   70,
                   draw.SANS_SERIF_NORMAL,
                   draw.TEXT_SIZE_NORMAL,
                   draw.TEXT_WEIGHT_MEDIUM,
                   draw.COLOR_BLUE)

            d.Text("Face Detected",
                   150,
                   -250,
                   draw.SERIF_NORMAL,
                   draw.TEXT_SIZE_SMALL,
                   draw.TEXT_WEIGHT_REGULAR,
                   draw.COLOR_GREEN)

            d.Circle(-33, 60, 2, draw.COLOR_BLACK, draw.THICK_WEIGHT_MEDIUM)
            for detection in face_results.detections:
                mp_drawing.draw_detection(image, detection)

        # Draw the Hand Landmark detection on the image.
        if ldk_result.multi_hand_landmarks:
            for hand_ldk in ldk_result.multi_hand_landmarks:
                for idx, dim in enumerate(hand_ldk.landmark):
                    xHand, yHand = int(dim.x * w), int(dim.y * h)

                    if (idx % 4 == 0) and (idx != 0):
                        d.Circle(xHand - int(h / 2), yHand - int(w / 2), 10, draw.COLOR_BLACK, draw.THICK_WEIGHT_BOLD)

                        # if (518 > xHand > 460) and (405 > yHand > 350):
                        #
                        #     post_data_ready = data_ready(temp_data)
                        #
                        #     res_post_status = postTemp(post_data_ready)
                        #
                        #     if res_post_status.status_code == 201:
                        #         d.Text("Data has recorded",
                        #                -100,
                        #                170,
                        #                draw.SANS_SERIF_SMALL,
                        #                draw.TEXT_SIZE_NORMAL,
                        #                draw.COLOR_YELLOW,
                        #                draw.TEXT_WEIGHT_MEDIUM)

                mp_drawing.draw_landmarks(image, hand_ldk, mp_hands.HAND_CONNECTIONS)

        # Show fps on window
        current_time = time.time()
        fps = int(1 / (current_time - previous_time))

        previous_time = current_time

        d.Text(f"{fps} fps",
               -200,
               -270,
               draw.SANS_SERIF_NORMAL,
               draw.TEXT_SIZE_REGULAR,
               draw.TEXT_WEIGHT_REGULAR,
               draw.COLOR_PURPLE)

        # Show Video and set title
        cv2.imshow(window_title, image)

        if cv2.waitKey(5) == ord("q"):
            break

    cap.release()
