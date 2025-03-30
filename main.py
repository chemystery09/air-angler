import math

import cv2
import mediapipe as mp

GAME_START = False
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
sensitivity_threshold = 10
previous_fingertip_positions = {}
fingertips = [8, 12, 16, 20]
fingerfirstknuckle = [5, 9, 13, 17]
previous_x_position = None
moving_left = False
moving_right = False
ok_threshold = 30

while True:
    success, image = cap.read()
    if not success:
        break
    frame = cv2.flip(image, 1)
    img_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_RGB)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if GAME_START is False:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_TIP
                ]
                thumb_x = int(thumb_tip.x * frame.shape[1])
                thumb_y = int(thumb_tip.y * frame.shape[0])
                index_x = int(index_tip.x * frame.shape[1])
                index_y = int(index_tip.y * frame.shape[0])
                distance = math.sqrt(
                    (index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2,
                )
                if distance < ok_threshold:
                    print("ok")
                    cv2.putText(
                        frame,
                        "OK Gesture Detected",
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )
                    GAME_START = True
            else:
                wrist_x = int(
                    hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
                    * frame.shape[1],
                )
                if previous_x_position is not None:
                    delta_x = wrist_x - previous_x_position
                    if abs(delta_x) >= sensitivity_threshold:
                        if delta_x < 0:  # Moving left if x decreases
                            moving_left = True
                            moving_right = False
                        else:
                            moving_left = False
                            moving_right = True
                    else:
                        moving_left = False
                        moving_right = False
                previous_x_position = wrist_x
                finger_folded = all(
                    hand_landmarks.landmark[fingertips[i]].y
                    > hand_landmarks.landmark[fingerfirstknuckle[i]].y
                    for i in range(4)
                )
                if finger_folded:
                    print("Fist detected")
                if moving_left:
                    print("Moving left")
                if moving_right:
                    print("Moving right")
    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
