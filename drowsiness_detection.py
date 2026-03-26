import cv2
import mediapipe as mp
import math
import numpy as np
import RPi.GPIO as GPIO

//GPiO detup
GPIO.setmode(GPIO.BCM)
LED_PIN = 23
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

//Helper Functions 
def euclidean_dist(p1, p2):
    return math.dist(p1, p2)

def eye_aspect_ratio(eye):
    A = euclidean_dist(eye[1], eye[5])
    B = euclidean_dist(eye[2], eye[4])
    C = euclidean_dist(eye[0], eye[3])
    return (A + B) / (2.0 * C)

//MediaPipe Setup 
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

//eye landmark
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
//camera
cap = cv2.VideoCapture(0)

//Drowsiness parameters
EYE_AR_THRESH = 0.16
CLOSED_FRAMES_THRESH = 20

closed_frames = 0
drowsy = False

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = face_mesh.process(rgb)

        if result.multi_face_landmarks:
            for face in result.multi_face_landmarks:

                left_eye = []
                right_eye = []

                //draw eye point
                for idx in LEFT_EYE:
                    x = int(face.landmark[idx].x * w)
                    y = int(face.landmark[idx].y * h)
                    left_eye.append((x, y))
                    cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)  # RED DOT

                for idx in RIGHT_EYE:
                    x = int(face.landmark[idx].x * w)
                    y = int(face.landmark[idx].y * h)
                    right_eye.append((x, y))
                    cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)  # RED DOT

                //draw eye boundary
                cv2.polylines(frame, [np.array(left_eye)], True, (255, 0, 0), 1)
                cv2.polylines(frame, [np.array(right_eye)], True, (255, 0, 0), 1)

                //ear calculation
                ear = (eye_aspect_ratio(left_eye) +
                       eye_aspect_ratio(right_eye)) / 2.0

               //drowsiness logic
                if ear < EYE_AR_THRESH:
                    closed_frames += 1
                else:
                    closed_frames = 0
                    drowsy = False
                    GPIO.output(LED_PIN, GPIO.LOW)

                if closed_frames >= CLOSED_FRAMES_THRESH:
                    drowsy = True
                    GPIO.output(LED_PIN, GPIO.HIGH)

              //display info
                cv2.putText(frame, f"EAR: {ear:.2f}",
                            (30, 40), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

                if drowsy:
                    cv2.putText(frame, "DROWSINESS ALERT!",
                                (30, 80), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 3)
                else:
                    cv2.putText(frame, "AWAKE",
                                (30, 80), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 0), 2)

        cv2.imshow("Drowsiness Detection (LED Alert)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
