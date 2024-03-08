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
        if num_line > 10:
            order = "crosswalk"
            array_vertices = [np.array(roi_vertices, np.int32)]
            cv2.fillPoly(frame, array_vertices, (240, 130, 50))
            
        else:
            order = "no crosswalk"
    
    
    
    # roi1_down = (height // 3) * 2
    # roi2_down = height
    
    # roi1_vertices = [(0, roi1_down), (0, roi1_down - 30), (width, roi1_down - 30), (width, roi1_down)]
    # roi2_vertices = [(0, roi2_down), (0, roi2_down - 30), (width, roi2_down - 30), (width, roi2_down)]
    
    # roi1_array_vertices = [np.array(roi1_vertices, np.int32)]
    # roi2_array_vertices = [np.array(roi2_vertices, np.int32)]
    
    # roi1_mask = np.zeros_like(blurred)
    # roi2_mask = np.zeros_like(blurred)
    
    # cv2.fillPoly(roi1_mask, roi1_array_vertices, 255)
    # cv2.fillPoly(roi2_mask, roi2_array_vertices, 255)
    
    # roi1 = cv2.bitwise_and(blurred, roi1_mask)
    # roi2 = cv2.bitwise_and(blurred, roi2_mask)
    
    # # Draw the ROIs
    # cv2.polylines(frame, roi1_array_vertices, True, yellow, 2)
    # cv2.polylines(frame, roi2_array_vertices, True, yellow, 2)
    
    # # Thresholding to create a binary image
    # _, binary1 = cv2.threshold(roi1, 200, 255, cv2.THRESH_BINARY)
    # _, binary2 = cv2.threshold(roi2, 200, 255, cv2.THRESH_BINARY)

    # # Find contours in the binary image
    # contours1, _ = cv2.findContours(binary1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours2, _ = cv2.findContours(binary2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # # Filter contours based on area (adjust the threshold as needed)
    # min_contour_area = 200
    # valid_contours1 = [cnt for cnt in contours1 if cv2.contourArea(cnt) > min_contour_area]
    # valid_contours2 = [cnt for cnt in contours2 if cv2.contourArea(cnt) > min_contour_area]

    # # Draw contours on the original frame
    # cv2.drawContours(frame, valid_contours1, -1, cyen, 2)
    # cv2.drawContours(frame, valid_contours2, -1, cyen, 2)

    # # Check if number of contours is greater than 5 or not
    # roi1_check = True if len(valid_contours1) > 5 else False
    # roi2_check = True if len(valid_contours2) > 5 else False
    
    # # Change color of ROI and get order 
    # order = "Not exist crosswalk"
    # if roi1_check:
    #     cv2.polylines(frame, roi1_array_vertices, True, magenta, 2)
    #     order = "Maybe exist crosswalk"
        
    #     if roi2_check:
    #         cv2.polylines(frame, roi2_array_vertices, True, magenta, 2)
    #         order = "Exist crosswalk"
            
    # # Show order
    # cv2.putText(frame, order, ((width // 2) - 60, roi1_down - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, magenta, 2)
    
    return frame, order