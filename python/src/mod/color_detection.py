# Import libraries
import cv2
import numpy as np
from mod import region_of_interest as ROI

# Declare variables
track_and_line_gap_left = 200
track_and_line_gap_right = 200

# Function for detect color
def detection(frame, best_pos, normal_pos):
    order = "no line"
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help with edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Define region of interests (ROI) to focus on the lines
    height, width = gray.shape
    roi_up = (height // 5) * 3
    roi_down = height - 30
    width_of_roi = (width - 200) // 2 
    roi1_vertices = [(0, roi_down), (0, roi_up), (width_of_roi, roi_up), (width_of_roi, roi_down)]
    roi2_vertices = [(width, roi_down), (width, roi_up), (width - width_of_roi, roi_up), (width - width_of_roi, roi_down)]
    roi1, frame = ROI.region_of_interest(blurred, frame, roi1_vertices)
    roi2, frame = ROI.region_of_interest(blurred, frame, roi2_vertices)
    roi = cv2.add(roi1, roi2)
    
    # Thresholding to create a binary image
    _, binary = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY)
    
    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the best contours
    if len(contours) is not 0:
        
        # Split biger contours
        min_contour_area = 200
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

        # Split right and left contours
        # and find nearest contour to center
        global right_contour, left_contour
        right_contour = None
        left_contour = None
        right_gap = width
        left_gap = 0
        for contour in valid_contours:
            m = cv2.moments(contour)
            center_x = int(m['m10'] / m['m00'])
            if center_x < width / 2: # Left contour
                if center_x > left_gap :
                    left_contour = contour
                    left_gap = center_x
            elif center_x > width / 2: # Right contour
                if center_x < right_gap :
                    right_contour = contour
                    right_gap = center_x
        
        # Find the track line
        global track_line
        track_line = None
        if (left_contour is not None) and (right_contour is not None):
            track_line = (left_gap + right_gap // 2, roi_up)
            cv2.drawContours(frame, [left_contour], -1, (6, 51, 235), 5)
            cv2.drawContours(frame, [right_contour], -1, (6, 51, 235), 5)
        elif left_contour is not None:
            track_line = (left_gap + track_and_line_gap_left, roi_up)
            cv2.drawContours(frame, [left_contour], -1, (6, 51, 235), 5)
        elif right_contour is not None:
            track_line = (right_gap - track_and_line_gap_right, roi_up)
            cv2.drawContours(frame, [right_contour], -1, (6, 51, 235), 5)
        else:
            track_line = None
    
        # Draw the track line
        if track_line is not None:
            cv2.line(frame, (width // 2, height), track_line, (255, 0, 255), 6)
            
            # Draw range of track lines
            best_range = (width - best_pos) // 2
            normal_range = (width - normal_pos) // 2
            cv2.line(frame, (best_range, roi_up + 20), (best_range, roi_up - 20), (77, 249, 117), 5)
            cv2.line(frame, (width - best_range, roi_up + 20), (width - best_range, roi_up - 20), (77, 249, 117), 5)
            cv2.line(frame, (normal_range, roi_up + 20), (normal_range, roi_up - 20), (80, 134, 240), 5)
            cv2.line(frame, (width - normal_range, roi_up + 20), (width - normal_range, roi_up - 20), (80, 134, 240), 5)
        
            # Get order
            track = track_line[0]
            if best_range <= track <= width - best_range:
                order = "forward"
            elif normal_range <= track < best_range:
                order = "right"
            elif width - best_range < track <= width - normal_range:
                order = "left"
            elif track < normal_range:
                order = "right right"
            elif width - normal_range < track:
                order = "left left"
            else:
                order = "no line"
                 
    return order