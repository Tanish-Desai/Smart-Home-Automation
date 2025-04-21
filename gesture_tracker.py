import cv2
import mediapipe as mp
# import serial_talker
import wifi_talker

BRIGHTNESS = 4
CONTRAST = 1

# Establish connection with the ESP32

wifi_talker.connect_socket()

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,  # Change to 2 if you want to process both hands.
    min_detection_confidence=0.9,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

def count_fingers(landmarks, hand_label="Right"):
    """
    Count which fingers are up.
    landmarks: list of 21 landmarks with format [id, cx, cy]
    Returns a list of 5 elements (thumb, index, middle, ring, pinky)
    with 1 indicating the finger is up and 0 otherwise.
    """
    fingers = []
    # Thumb: for right hand, tip (4) should be to the right of landmark 3; for left hand, the opposite.
    if hand_label == "Right":
        if landmarks[4][1] > landmarks[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    else:
        if landmarks[4][1] < landmarks[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    # Other four fingers: if tip is above (i.e., smaller y value) the landmark two indices before, the finger is open.
    for tip in [8, 12, 16, 20]:
        if landmarks[tip][2] < landmarks[tip - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def get_hand_label(results):
    """Determine hand label ('Right' or 'Left') from the handedness classification."""
    if results.multi_handedness:
        # The classification score and label are stored for each detected hand.
        # For a single hand, we can take the first result.
        return results.multi_handedness[0].classification[0].label
    return "Right"  # default

# gestures for right hand. Reverse sort for left-hand
# for thumb, 1 means closed, 0 means open
gestures = {
    "open" : [0,1,1,1,1],
    "fist" : [1,0,0,0,0],
    "index-thumb up" : [0,1,0,0,0],
    "index down thumb" : [0,0,0,0,0],
    "yo" : [0,1,0,0,1],
    "ilu" : [1,1,0,0,1],
    "3_out" : [1,1,1,1,0],
    "1_out" : [1,1,0,0,0],
    "pinky_out" : [1,0,0,0,1]
}

"""
open -> door open
fist -> door close
3_out -> fan on
2_out -> fan off

"""

def get_gesture(sign):
    for ges in gestures:
        if gestures[ges] == sign:
            return ges
    for ges in gestures:
        leftie = sorted(gestures[ges], reverse=True)
        if leftie == sign:
            return "left" + ges
    return None

# Open the webcam.
cap = cv2.VideoCapture(0)

# memory for hand gesture to not repeat signal unnecessarily
gesture_memory = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB for MediaPipe.
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Add brightness and constrast to image
    frame_rgb = cv2.convertScaleAbs(frame_rgb, CONTRAST, BRIGHTNESS)
    frame = cv2.convertScaleAbs(frame, CONTRAST, BRIGHTNESS)
    # Process the frame and detect hand landmarks.
    results = hands.process(frame_rgb)
    
    landmarks_list = []
    if results.multi_hand_landmarks:
        # Use handedness info to adjust thumb logic (if needed).
        hand_label = get_hand_label(results)
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the frame.
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Extract landmark positions in pixel coordinates.
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
            landmarks_list = lm_list  # For simplicity, consider only the first detected hand.

        if landmarks_list:
            # Get finger status as a list of 0s and 1s.
            fingers = count_fingers(landmarks_list, hand_label)
            # Example: if only the index finger is up, fingers might be [0, 1, 0, 0, 0]
            cv2.putText(frame, f"Fingers: {fingers}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 60), 2)
            
            """
            # Check for specific gesture: only index finger up.
            if fingers == [0, 1, 0, 0, 0]:
                cv2.putText(frame, "One Finger Up Detected!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2)
                # typer.type("One Finger Up")
            """
            gesture_result = get_gesture(fingers)
            if gesture_result!=gesture_memory:
                if gesture_memory != gesture_result:
                    if gesture_result == "index-thumb up":
                        # serial_talker.send_data("on")
                        wifi_talker.send_data("led_on")
                        # wifi_talker.send_data("angle: 90")
                    elif gesture_result == "index down thumb":
                        # serial_talker.send_data("off")
                        wifi_talker.send_data("led_off")
                        # wifi_talker.send_data("angle: 0")
                    elif gesture_result == "open":
                        wifi_talker.send_data("angle: 90")
                    elif gesture_result == "fist":
                        wifi_talker.send_data("angle: 0")
                    elif gesture_result == "3_out":
                        wifi_talker.send_data("motor_on")
                    elif gesture_result == "1_out":
                        wifi_talker.send_data("motor_off")
                gesture_memory=gesture_result

            # serial_response = serial_talker.read_data()
            # if serial_response:
            #     print(f"Received (Serial) : {serial_response}\n")
                
            # wifi_response = wifi_talker.read_data()
            # if wifi_response:
            #     print(f"Received (WiFi) : {wifi_response}\n")
    
    cv2.imshow("Hand Gesture Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# serial_talker.close_serial()
wifi_talker.close_socket()
cap.release()
cv2.destroyAllWindows()
