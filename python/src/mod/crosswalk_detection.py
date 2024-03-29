# Import libraries
import cv2
import numpy as np
from mod import region_of_interest as ROI

# Function to detect crosswalk
def crosswalk_detection(frame):
    order = "no crosswalk"
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help with edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection using canny
    edges = cv2.Canny(blurred, 50, 150)
    
    # Define region of interests (ROI) to focus on crosswalk lines
    height, width = gray.shape
    roi_up = height - 30
    
    roi_vertices = [(0, height), (0, roi_up), (width, roi_up), (width, height)]
    fme = frame.copy()
    roi, _ = ROI.region_of_interest(edges, fme, roi_vertices)
    
    # Use HoughLines to detect lines in the image
    lines= cv2.HoughLinesP(roi, 1, np.pi/180, threshold=25, minLineLength=20, maxLineGap=20)
    
    # Draw the detected lines on the original image
    if lines is not None:
        num_line = 0
        for line in lines:
            x1, y1, x2, y2 = line[0]
            theta = abs(y2 - y1) / abs(x2 - x1) 
            
            # Separate lines that are not horizontal
            if theta >= 1:
                num_line += 1
                
                # debuging
                cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
        
        # Get order
        if num_line > 6:
            order = "crosswalk"
            array_vertices = [np.array(roi_vertices, np.int32)]
            cv2.fillPoly(frame, array_vertices, (240, 130, 50))
            
        else:
            order = "no crosswalk"
    
    return frame, order