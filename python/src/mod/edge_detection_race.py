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
    frame_th = frame.copy()
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help with edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    blurred_th = blurred.copy()
    
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
    
    # Define region of interests (ROI) to focus on the lines (threshold)
    roi1_th, _ = ROI.region_of_interest(blurred_th, frame_th, roi1_vertices)
    roi2_th, _ = ROI.region_of_interest(blurred_th, frame_th, roi2_vertices)
    roi_th = cv2.add(roi1_th, roi2_th)
    
    # Use HoughLines to detect lines in the image
    # threshold: The minimum number of intersections to "*detect*" a line
    # minLineLength: The minimum number of points that can form a line. Lines with less than this number of points are disregarded.
    # maxLineGap: The maximum gap between two points to be considered in the same line.
    lines= cv2.HoughLinesP(roi, 1, np.pi/180, threshold=30, minLineLength=10, maxLineGap=30)

    # Thresholding to create a binary image
    _, binary = cv2.threshold(roi_th, 200, 255, cv2.THRESH_BINARY)
    
    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the line edges
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
    
    # Find the line contours
    if len(contours) is not 0:
        
        # Split biger contours
        min_contour_area = 500
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
                
        # Find the contour that contains lines
        # and draw them
        global left_contain_line, right_contain_line
        left_contain_line = False
        right_contain_line = False
        m1 = cv2.moments(left_contour)
        m2 = cv2.moments(right_contour)
        center_left = [int(m1['m10'] / m1['m00']), int(m1['m01'] / m1['m00'])]
        center_right = [int(m2['m10'] / m2['m00']), int(m2['m01'] / m2['m00'])]
        if len(left_lines) is not 0:
            for line in left_lines:
                x1, y1, x2, y2, cx, cy = line
                if center_left[0] - 20 < cx < center_left[0] + 20:
                    if center_left[1] - 20 < cy < center_left[1] + 20:
                        cv2.line(frame, (x1, y1), (x2, y2), (36, 51, 235), 5)
                        left_contain_line = True
            for line in right_lines:
                x1, y1, x2, y2, cx, cy = line
                if center_right[0] - 20 < cx < center_right[0] + 20:
                    if center_right[1] - 20 < cx < center_right[1] + 20:
                        cv2.line(frame, (x1, y1), (x2, y2), (36, 51, 235), 5)
                        right_contain_line = True
    
        # Draw the contours that contain lines
        if left_contain_line:
            cv2.drawContours(frame, left_contour, -1, (255, 255, 255), 5)
        if right_contain_line:
            cv2.drawContours(frame, right_contour, -1, (255, 255, 255), 5)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # # Draw the detected lines on the original image
    # if lines is not None:
    #     left_lines = []
    #     right_lines = []
    #     for line in lines:
    #         x1, y1, x2, y2 = line[0]
    #         theta = abs(y2 - y1) / abs(x2 - x1) 
    #         # Separate lines that are not vectorizental
    #         if theta >= 0.3:
    #             line_center = (abs(x1 + x2) // 2, abs(y1 + y2) // 2)
    #             line = np.append(line, [line_center[0], line_center[1]])
                
    #             # Separate lines into right and left
    #             if line_center[0] > (width / 2):
    #                 right_lines.append(line)
    #             else:
    #                 left_lines.append(line)
                    
    #         # debuging
    #         # else:
    #         #     cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
        
    #     # Find the nearest line to the center of frame
    #     left_distance = 0
    #     right_distance = width
    #     global left_line, right_line
    #     left_line = None
    #     right_line = None
        
    #     for line in left_lines:
    #         x1, y1, x2, y2, left_center_x, _ = line
    #         if left_center_x > left_distance:
    #             left_distance = left_center_x
    #             left_line = line
                
    #     for line in right_lines:
    #         x1, y1, x2, y2, right_enter_x, _ = line
    #         if right_enter_x < right_distance:
    #             right_distance = right_enter_x
    #             right_line = line

    #     # Draw the lines
    #     global left_edge, right_edge
    #     left_edge, right_edge = None, None
    #     if left_line is not None:
    #         x1, y1, x2, y2, cx, _ = left_line
    #         left_edge = cx
    #         cv2.line(frame, (x1, y1), (x2, y2), (36, 51, 235), 5)
            
    #     if right_line is not None:
    #         x1, y1, x2, y2, cx, _ = right_line
    #         right_edge = cx
    #         cv2.line(frame, (x1, y1), (x2, y2), (36, 51, 235), 5)
        
    #     # Find the track line
    #     if left_edge is not None and right_edge is not None:
    #         track_line = ((left_edge + right_edge) // 2, roi_up)
            
    #     elif right_edge is not None:
    #         track_line = ((right_edge - gap_right_edge), roi_up)
            
    #     elif left_edge is not None:
    #         track_line = ((left_edge + gap_left_edge), roi_up)
            
    #     else:
    #         track_line = None
    
    #     # Draw the track line
    #     if track_line is not None:
    #         cv2.line(frame, (width // 2, height), track_line, (255, 0, 255), 6)
            
    #         # Draw range of track line
    #         track_range = (width - 50) // 2
    #         cv2.line(frame, (track_range, roi_up + 20), (track_range, roi_up - 20), (77, 249, 117), 5)
    #         cv2.line(frame, (width - track_range, roi_up + 20), (width - track_range, roi_up - 20), (77, 249, 117), 5)
            
    #         # Change camera state
    #         track = track_line[0]
    #         if track < track_range:
    #             last_angle += 2
    #             servo.angle = last_angle
    #         elif width - track_range < track:
    #             last_angle -= 2
    #             servo.angle = last_angle
            
    #         # Send order
    #         if -20 <= last_angle <= 0:
    #             order = "forward"
    #         elif -30 <= last_angle < -20:
    #             order = "left"
    #         elif 0 < last_angle <= 10:
    #             order = "right"
    #         elif last_angle < -30:
    #             order = "left left"
    #         elif 10 < last_angle:
    #             order = "right right"
    #         else:
    #             order = "no line"

    return order, last_angle