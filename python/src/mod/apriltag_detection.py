# Import libraries
from pupil_apriltags import Detector
import cv2
import math
detector = Detector(families='tag36h11')

# Mach labels and april tags
labels = {
    0: 'tunnel Beginning',
    1: 'tunnel End',
    2: 'cross walk',
    3: 'parking zone',
    # 4: 'No-Passing Zone',
    # 5: 'Passing Zone',
    6: 'stop',
    # 7: 'priority over',
    # 8: 'Bared area',
    # 9: 'step uphill',
    # 10: 'step downhill',
    11: 'turn left',
    12: 'turn right',
    119: 'go straight',
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
        
        if size >= 40:
            if size > main_size:
                nearest_apriltag = detection
                main_size = size
    
    # Show nearest apriltag
    label = 'no label found'
    if nearest_apriltag is not None:
        cv2.polylines(frame, [nearest_apriltag.corners.astype(int)], True, (240, 130, 50), 2)
        
        # Find label and get order
        try:
            label = labels[nearest_apriltag.tag_id]
        except:
            pass
    
    return frame, label