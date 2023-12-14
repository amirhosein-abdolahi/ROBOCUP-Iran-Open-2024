import cv2
import numpy as np
from pupil_apriltags import Detector

def detect_apriltags_webcam():
    # AprileTags labels
    labels = {
        0: 'Tunnel Beginning',
        1: 'Tunnel End',
        2: 'Cross walk',
        3: 'Parking zone',
        4: 'No-Passing Zone',
        5: 'Passing Zone',
        6: 'stop',
        7: 'priority over',
        8: 'Bared area',
        9: 'step uphill',
        10: 'step downhill',
        11: 'turn left',
        12: 'turn right',
        13: 'go straight',
    }

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
            cv2.polylines(frame, [detection.corners.astype(int)], True, (255, 255, 0), 2)
            
            # Set label 
            try:
                label = labels[detection.tag_id]
            except:
                label = 'No label found'
            cv2.putText(frame, label, (int(detection.center[0]), int(detection.center[1])),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

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
