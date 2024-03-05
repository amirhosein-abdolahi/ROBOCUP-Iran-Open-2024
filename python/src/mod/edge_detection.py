# Import ibrari
from turtle import left
import cv2
import numpy as np

# Function to detrect edges
def edge_detection(frame):
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help with edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection using canny
    edges = cv2.Canny(blurred, 50, 150)
    
    # Define region of interests (ROI) to focus on the lines
    height, width = gray.shape
    roi_up = (height // 3) * 2
    roi_down = height - 30
    roi_vertices = [(0, roi_down), (0, roi_up), (width, roi_up), (width, roi_down)]
    roi_array_vertices = [np.array(roi_vertices, np.int32)]
    roi_mask = np.zeros_like(edges)
    cv2.fillPoly(roi_mask, roi_array_vertices, 255)
    roi = cv2.bitwise_and(edges, roi_mask)
    
    # Draw the ROI
    cv2.polylines(frame, roi_array_vertices, True, (255, 0, 0), 2)
    
    # Use HoughLines to detect lines in the image
    # threshold: The minimum number of intersections to "*detect*" a line
    # minLineLength: The minimum number of points that can form a line. Lines with less than this number of points are disregarded.
    # maxLineGap: The maximum gap between two points to be considered in the same line.
    lines = cv2.HoughLinesP(roi, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=30)

    # Draw the detected lines on the original image
    if lines is not None:
        left_lines = []
        right_lines = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Separate lines that are not horizontal
            if abs(y1 - y2) > 40:
                line_center = (abs(x1 + x2) // 2, abs(y1 + y2) // 2)
                line = np.append(line, [line_center[0], line_center[1]])
                
                # Separate lines into right and left
                if line_center[0] > (width / 2):
                    right_lines.append(line)
                else:
                    left_lines.append(line)
        
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
            x1, y1, x2, y2, cx, cy = left_line
            left_edge = cx
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
            cv2.circle(frame, (cx, cy), 4, (255, 0, 0), 2)
            
            # This code is for find uper dot
            # if y1 < y2:
            #     left_edge = x1
            #     cv2.circle(frame, (x1, y1), 4, (255, 0, 0), 2)
            # else:
            #     left_edge = x2
            #     cv2.circle(frame, (x2, y2), 4, (255, 0, 0), 2)
            
        if right_line is not None:
            x1, y1, x2, y2, cx, cy = right_line
            right_edge = cx
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
            cv2.circle(frame, (cx, cy), 4, (255, 0, 0), 2)
            
            # This code is for find uper dot
            # if y1 < y2:
            #     left_edge = x1
            #     cv2.circle(frame, (x1, y1), 4, (255, 0, 0), 2)
            # else:
            #     left_edge = x2
            #     cv2.circle(frame, (x2, y2), 4, (255, 0, 0), 2)
            
        # Find the track line
        if left_edge is not None and right_edge is not None:
            track_line = ((left_edge + right_edge) // 2, roi_up)
            
        elif right_edge is not None:
            track_line = ((right_edge - 250), roi_up)
            
        elif left_edge is not None:
            track_line = ((left_edge + 250), roi_up)
            
        else:
            track_line = None
        
        # Draw the track line
        if track_line is not None:
            cv2.line(frame, (width // 2, height), track_line, (255, 0, 255), 5)
            


    order = ""
    return frame, order