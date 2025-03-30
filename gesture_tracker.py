import cv2
import mediapipe as mp
import typer


# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,  # Change to 2 if you want to process both hands.
    min_detection_confidence=0.7,
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

# Open the webcam.
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB for MediaPipe.
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
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
                        1, (180, 255, 255), 2)
            # Check for specific gesture: only index finger up.
            if fingers == [0, 1, 0, 0, 0]:
                cv2.putText(frame, "One Finger Up Detected!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2)
                # typer.type("One Finger Up")
    
    cv2.imshow("Hand Gesture Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
