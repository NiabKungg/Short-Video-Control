import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui
import time

# Mediapipe hand connections (used to draw lines between landmarks)
HAND_CONNECTIONS = mp.solutions.hands.HAND_CONNECTIONS
skip = False
like = False
undo = False

# Function to draw hand landmarks and connections on the image
def draw_landmarks_on_image(image, detection_result):
    global like, skip, undo
    annotated_image = image.copy()  # Create a copy of the original image
    height, width, _ = image.shape
    pressed = False  # Initialize pressed variable
    last_press_time = 0  # Initialize last press time
    clicking = False  # Initialize clicking status
    click_start_time = 0  # Initialize click start time

    # Loop through each detected hand and draw the landmarks
    for hand_landmark in detection_result.hand_landmarks:
        # Draw landmarks and labels
        for idx, landmark in enumerate(hand_landmark):
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            # Draw a circle for each landmark point
            cv2.circle(annotated_image, (x, y), 5, (0, 255, 0), -1)
            # Display the index number of the landmark
            cv2.putText(annotated_image, f'{idx}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Draw connections between landmarks to form the hand structure
        for connection in HAND_CONNECTIONS:
            start_idx = connection[0]
            end_idx = connection[1]
            start_point = (int(hand_landmark[start_idx].x * width), int(hand_landmark[start_idx].y * height))
            end_point = (int(hand_landmark[end_idx].x * width), int(hand_landmark[end_idx].y * height))
            cv2.line(annotated_image, start_point, end_point, (255, 0, 0), 2)  # Draw lines between landmarks

        # Calculate pixel positions for landmarks 4, 8, and 12
        landmark_4 = hand_landmark[4]
        landmark_8 = hand_landmark[8]
        landmark_12 = hand_landmark[12]

        # Convert normalized coordinates to pixel coordinates
        x4 = int(landmark_4.x * width)
        y4 = int(landmark_4.y * height)
        x8 = int(landmark_8.x * width)
        y8 = int(landmark_8.y * height)
        x12 = int(landmark_12.x * width)
        y12 = int(landmark_12.y * height)

        # Draw line between landmark 4 and landmark 8
        cv2.line(annotated_image, (x4, y4), (x8, y8), (0, 255, 255), 2)  # Yellow line between landmark 4 and 8

        # Draw line between landmark 12 and landmark 8
        cv2.line(annotated_image, (x12, y12), (x8, y8), (255, 0, 255), 2)  # Magenta line between landmark 12 and 8

        # Calculate distance in pixels between landmarks 4 and 8
        distance_pixels_4_8 = np.sqrt((x8 - x4) ** 2 + (y8 - y4) ** 2)

        # Calculate distance in pixels between landmarks 12 and 8
        distance_pixels_12_8 = np.sqrt((x12 - x8) ** 2 + (y12 - y8) ** 2)

        # Calculate percentage distances (relative to image size)
        distance_percentage_4_8 = ((distance_pixels_4_8 / np.sqrt(width ** 2 + height ** 2)) * 100) * 10
        distance_percentage_12_8 = ((distance_pixels_12_8 / np.sqrt(width ** 2 + height ** 2)) * 100) * 10

        # Display the distance percentages
        if like:
            cv2.putText(annotated_image, f'Like Video!!!', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        elif skip:
            cv2.putText(annotated_image, f'Skip Video!!!', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        elif undo:
            cv2.putText(annotated_image, f'Back Video!!!', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.putText(annotated_image, f'Distance 4-8: {distance_percentage_4_8:.2f}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(annotated_image, f'Distance 12-8: {distance_percentage_12_8:.2f}%', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Check if the distance percentage between 4 and 8 is less than 20
        if distance_percentage_4_8 < 20:
            pyautogui.press('down')
            pressed = True
            skip = True

        if distance_percentage_12_8 < 20:
            pyautogui.press('up')
            undo = True


        # Reset pressed status if distance_percentage is 20 or more
        if distance_percentage_4_8 >= 20:
            pressed = False  # Reset pressed status
            skip = False

        if distance_percentage_12_8 >= 20:
            undo = False

        # Check if distance percentage between 4 and 8 is greater than 150
        if distance_percentage_4_8 > 150 and not clicking:
            pyautogui.click()
            pyautogui.click()
            clicking = False
            like = True

            # Perform mouse click every 0.1 seconds (or your desired interval)
            current_time = time.time()
            if current_time - click_start_time >= 0.1:  # Change 0.1 to adjust click frequency
                pyautogui.click()  # Simulate mouse click
                click_start_time = current_time  # Update click start time

        # Stop clicking if distance_percentage is 150 or less
        if distance_percentage_4_8 <= 150:
            clicking = True
            like = False

    return annotated_image

# STEP 2: Create a HandLandmarker object.
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

# STEP 3: Initialize webcam
cap = cv2.VideoCapture(0)

# STEP 4: Process each frame from the webcam
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert the BGR frame (from OpenCV) to RGB (Mediapipe works with RGB)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

    # Detect hand landmarks from the current frame
    detection_result = detector.detect(mp_image)

    # Draw landmarks on the frame
    annotated_image = draw_landmarks_on_image(frame, detection_result)

    # Display the frame
    cv2.imshow('Hand Landmarks', annotated_image)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# STEP 5: Release the webcam and close the windows
cap.release()
cv2.destroyAllWindows()
