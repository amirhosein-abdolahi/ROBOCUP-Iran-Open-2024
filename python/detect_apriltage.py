import cv2
import numpy as np
from pupil_apriltags import Detector

def detect_apriltags_webcam():
    # Open a connection to the webcam (you can change the index if you have multiple cameras)
    cap = cv2.VideoCapture(0)

    # Create an AprilTags detector
    detector = Detector(families='tag36h11')

    while True:
        # Capture frame from the webcam
        ret, frame = cap.read()
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect AprilTags in the frame
        detections = detector.detect(gray, estimate_tag_pose=False)

        # Draw the AprilTags on the frame
        for detection in detections:
            for point in detection.corners:
                pt = tuple(map(int, point))
                cv2.circle(frame, pt, 5, (0, 255, 0), -1)
            cv2.polylines(frame, [detection.corners.astype(int)], True, (0, 255, 0), 2)
            cv2.putText(frame, f"ID: {detection.tag_id}", (int(detection.center[0]), int(detection.center[1])),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame with AprilTag detections
        cv2.imshow('AprilTag Detection', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

# Call the function to detect AprilTags from the webcam
detect_apriltags_webcam()
