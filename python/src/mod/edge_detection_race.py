# Import libraries
import cv2
import numpy as np
from mod import region_of_interest as ROI

# Define some variables
gap_right_edge = 200
gap_left_edge = 200

# Function to detect edges
def detection(frame, servo, last_angle):
    order = "no line"
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise and help with edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Perform edge detection using canny
    edges = cv2.Canny(blurred, 50, 150)
    
    # Define region of interests (ROI) to focus on the lines
    height, width = gray.shape
    roi_up = (height // 5) * 3
    roi_down = height - 30
    width_of_roi = (width - 200) // 2 
    roi1_vertices = [(0, roi_down), (0, roi_up), (width_of_roi, roi_up), (width_of_roi, roi_down)]
    roi2_vertices = [(width, roi_down), (width, roi_up), (width - width_of_roi, roi_up), (width - width_of_roi, roi_down)]
    roi1, frame = ROI.region_of_interest(edges, frame, roi1_vertices)
    roi2, frame = ROI.region_of_interest(edges, frame, roi2_vertices)
    roi = cv2.add(roi1, roi2)
    
    # Use HoughLines to detect lines in the image
    # threshold: The minimum number of intersections to "*detect*" a line
    # minLineLength: The minimum number of points that can form a line. Lines with less than this number of points are disregarded.
    # maxLineGap: The maximum gap between two points to be considered in the same line.
    lines= cv2.HoughLinesP(roi, 1, np.pi/180, threshold=30, minLineLength=10, maxLineGap=30)
    
    # Draw the detected lines on the original image
    if lines is not None:
        left_lines = []
        right_lines = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            theta = abs(y2 - y1) / abs(x2 - x1) 
            
            # Separate lines that are not vectorizental
            if theta >= 0.3:
                line_center = (abs(x1 + x2) // 2, abs(y1 + y2) // 2)
                line = np.append(line, [line_center[0], line_center[1]])
                
                # Separate lines into right and left
                if line_center[0] > (width / 2):
                    right_lines.append(line)
                else:
                    left_lines.append(line)
                    
            # debuging
            # else:
            #     cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
        
        # Find the nearest line to the center of frame
        left_distance = 0
        right_distance = width
        global left_line, right_line
        left_line = None
        right_line = None
        
        for line in left_lines:
            x1, y1, x2, y2, left_center_x, _ = line
            if left_center_x > left_distance:
                left_distance = left_center_x
                left_line = line
                
        for line in right_lines:
            x1, y1, x2, y2, right_enter_x, _ = line
            if right_enter_x < right_distance:
                right_distance = right_enter_x
                right_line = line
                
        # Draw the lines
        global left_edge, right_edge
        left_edge, right_edge = None, None
        if left_line is not None:
            x1, y1, x2, y2, cx, _ = left_line
            left_edge = cx
            cv2.line(frame, (x1, y1), (x2, y2), (36, 51, 235), 5)
            
        if right_line is not None:
            x1, y1, x2, y2, cx, _ = right_line
            right_edge = cx
            cv2.line(frame, (x1, y1), (x2, y2), (36, 51, 235), 5)
        
        # Find the track line
        if left_edge is not None and right_edge is not None:
            track_line = ((left_edge + right_edge) // 2, roi_up)
            
        elif right_edge is not None:
            track_line = ((right_edge - gap_right_edge), roi_up)
            
        elif left_edge is not None:
            track_line = ((left_edge + gap_left_edge), roi_up)
            
        else:
            track_line = None
    
        # Draw the track line
        if track_line is not None:
            cv2.line(frame, (width // 2, height), track_line, (255, 0, 255), 6)
            
            # Draw range of track line
            track_range = (width - 40) // 2
            cv2.line(frame, (track_range, roi_up + 20), (track_range, roi_up - 20), (77, 249, 117), 5)
            cv2.line(frame, (width - track_range, roi_up + 20), (width - track_range, roi_up - 20), (77, 249, 117), 5)
            
            # Change camera state
            track = track_line[0]
            if track < track_range:
                last_angle += 2
                servo.angle = last_angle
            elif width - track_range < track:
                last_angle -= 2
                servo.angle = last_angle
            
            # Send order
            if -35 <= last_angle <= 15:
                order = "forward"
            elif -45 <= last_angle < -35:
                order = "left"
            elif 15 < last_angle <= 25:
                order = "right"
            elif last_angle < -45:
                order = "left left"
            elif 25 < last_angle:
                order = "right right"
            else:
                order = "no line"
            
    return order, last_angle
