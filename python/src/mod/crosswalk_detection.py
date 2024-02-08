# Import libraries
import cv2
import numpy as np

# Define colors
red = (0, 0, 255)
blue = (255, 0, 0)
green = (0, 255, 0)
cyen = (255, 255, 0)
magenta = (255, 0, 255)
yellow = (0, 255, 255)

# Function to detect crosswalk
def crosswalk_detection(frame):
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help with edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Define region of interests (ROI) to focus on crosswalk lines
    height, width = gray.shape
    roi1_down = (height // 3) * 2
    roi2_down = height
    
    roi1_vertices = [(0, roi1_down), (0, roi1_down - 30), (width, roi1_down - 30), (width, roi1_down)]
    roi2_vertices = [(0, roi2_down), (0, roi2_down - 30), (width, roi2_down - 30), (width, roi2_down)]
    
    roi1_array_vertices = [np.array(roi1_vertices, np.int32)]
    roi2_array_vertices = [np.array(roi2_vertices, np.int32)]
    
    roi1_mask = np.zeros_like(blurred)
    roi2_mask = np.zeros_like(blurred)
    
    cv2.fillPoly(roi1_mask, roi1_array_vertices, 255)
    cv2.fillPoly(roi2_mask, roi2_array_vertices, 255)
    
    roi1 = cv2.bitwise_and(blurred, roi1_mask)
    roi2 = cv2.bitwise_and(blurred, roi2_mask)
    
    # Draw the ROIs
    cv2.polylines(frame, roi1_array_vertices, True, yellow, 2)
    cv2.polylines(frame, roi2_array_vertices, True, yellow, 2)
    
    # Thresholding to create a binary image
    _, binary1 = cv2.threshold(roi1, 200, 255, cv2.THRESH_BINARY)
    _, binary2 = cv2.threshold(roi2, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours1, _ = cv2.findContours(binary1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(binary2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area (adjust the threshold as needed)
    min_contour_area = 500
    valid_contours1 = [cnt for cnt in contours1 if cv2.contourArea(cnt) > min_contour_area]
    valid_contours2 = [cnt for cnt in contours2 if cv2.contourArea(cnt) > min_contour_area]

    # Draw contours on the original frame
    cv2.drawContours(frame, valid_contours1, -1, cyen, 2)
    cv2.drawContours(frame, valid_contours2, -1, cyen, 2)

    # Check if number of contours is greater than 5 or not
    roi1_check = True if len(valid_contours1) > 5 else False
    roi2_check = True if len(valid_contours2) > 5 else False
    
    # Change color of ROI and get order 
    order = "Not exist crosswalk"
    if roi1_check:
        cv2.polylines(frame, roi1_array_vertices, True, magenta, 2)
        order = "Maybe exist crosswalk"
        
        if roi2_check:
            cv2.polylines(frame, roi2_array_vertices, True, magenta, 2)
            order = "Exist crosswalk"
            
    # Show order
    cv2.putText(frame, order, ((width // 2) - 60, roi1_down - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, magenta, 2)
    
    return frame, order