# Import libraries
# from ast import main
# from operator import ne
# from numpy import size
from pupil_apriltags import Detector
import cv2
import math
detector = Detector(families='tag36h11')

# Define colors
red = (0, 0, 255)
blue = (255, 0, 0)
green = (0, 255, 0)
cyen = (255, 255, 0)
magenta = (255, 0, 255)
yellow = (0, 255, 255)

# Mach labels and april tags
labels = {
    0: 'Tunnel Beginning', # Important
    1: 'Tunnel End', # Important
    2: 'Cross walk', # Important
    3: 'Parking zone', # Important
    4: 'No-Passing Zone',
    5: 'Passing Zone',
    6: 'stop', # Important
    7: 'priority over',
    8: 'Bared area',
    9: 'step uphill',
    10: 'step downhill',
    11: 'turn left', # Important
    12: 'turn right', # Important
    119: 'go straight', # Important
}

# Functions for detect apriltag
def apriltag_detection(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect AprilTags in the frame
    detections = detector.detect(gray, estimate_tag_pose=False)
    
    # Find the nearest apriltag
    main_size = 0
    nearest_apriltag = None
    for detection in detections:
        corners = [detection.corners.astype(int)]
        dot1 = [corners[0][0][0], corners[0][0][1]]
        dot2 = [corners[0][2][0], corners[0][2][1]]
        size = int(math.dist(dot2, dot1))
        
        if size > main_size:
            nearest_apriltag = detection
            main_size = size
    
    # Show nearest apriltag
    label = 'No label found'
    if nearest_apriltag:
        cv2.polylines(frame, [nearest_apriltag.corners.astype(int)], True, blue, 2)
        
        # Find label and get order
        try:
            label = labels[nearest_apriltag.tag_id]
        except:
            pass
        cv2.putText(frame, label,
                    (int(nearest_apriltag.center[0]), int(nearest_apriltag.center[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
    
    return frame, labels