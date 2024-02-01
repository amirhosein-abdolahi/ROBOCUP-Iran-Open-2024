# import libraries
import cv2
import numpy as np
from statistics import mean

# Gap size between one line and center
line_gap = None

# Function to detect lines
def line_detection(frame):
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help with edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Define region of interests (ROI) to focus on the lines
    height, width = blurred.shape
    roi_up = (height // 3) * 2
    roi_down = height - 30
    
    roi1_vertices = [(0, roi_down), (0, roi_up) ,(width // 4, roi_up), (width // 4, roi_down)]
    roi2_vertices = [((width // 4) * 3, roi_down), ((width // 4) * 3, roi_up) ,(width, roi_up), (width, roi_down)]
    
    roi1_array_vertices = [np.array(roi1_vertices, np.int32)]
    roi2_array_vertices = [np.array(roi2_vertices, np.int32)]
    
    roi1_mask = np.zeros_like(blurred)
    roi2_mask = np.zeros_like(blurred)
    
    cv2.fillPoly(roi1_mask, roi1_array_vertices, 255)
    cv2.fillPoly(roi2_mask, roi2_array_vertices, 255)
    
    roi1 = cv2.bitwise_and(blurred, roi1_mask)
    roi2 = cv2.bitwise_and(blurred, roi2_mask)
    
    
    # Draw the ROIs
    cv2.polylines(frame, roi1_array_vertices, True, (255, 0, 0), 2)
    cv2.polylines(frame, roi2_array_vertices, True, (255, 0, 0), 2)
    

    # Draw two edge lines
    left_edge = (width // 2) - 20
    right_edge = (width // 2) + 20
    cv2.line(frame, (left_edge, roi_up), (left_edge, roi_down), (255, 0, 255), 2)
    cv2.line(frame, (right_edge, roi_up), (right_edge, roi_down), (255, 0, 255), 2)
    
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
    cv2.drawContours(frame, valid_contours1, -1, (0, 255, 0), 2)
    cv2.drawContours(frame, valid_contours2, -1, (0, 255, 0), 2)

    # Find the contour's center
    right_centers = [[], []]
    left_centers = [[], []]
    for contour in valid_contours1:
        m = cv2.moments(contour)
        cx = int(m['m10'] / m['m00'])
        cy = int(m['m01'] / m['m00'])
        left_centers[0].append(cx)
        left_centers[1].append(cy)
        cv2.line(frame, (cx, cy + 8), (cx, cy - 8), (0, 0, 255), 2)
        cv2.line(frame, (cx + 8, cy), (cx - 8, cy), (0, 0, 255), 2)

    for contour in valid_contours2:
        m = cv2.moments(contour)
        cx = int(m['m10'] / m['m00'])
        cy = int(m['m01'] / m['m00'])
        right_centers[0].append(cx)
        right_centers[1].append(cy)
        cv2.line(frame, (cx, cy + 8), (cx, cy - 8), (0, 0, 255), 2)
        cv2.line(frame, (cx + 8, cy), (cx - 8, cy), (0, 0, 255), 2)
        
    #     # Clustering center of contours to left and right side
    #     if cx < width / 2:
    #         left_centers[0].append(cx)
    #         left_centers[1].append(cy)

    #     elif cx > width / 2:
    #         right_centers[0].append(cx)
    #         right_centers[1].append(cy)
            
    # Get mean of left centers and right centers
    left_center = None
    right_center = None
    try :
        left_center = (int(mean(left_centers[0])), int(mean(left_centers[1])))
        cv2.circle(frame, left_center, 5, (0, 255, 255), 2)
    except :
        left_center = None

    try :
        right_center = (int(mean(right_centers[0])), int(mean(right_centers[1])))
        cv2.circle(frame, right_center, 5, (0, 255, 255), 2)
    except :
        right_center = None
        
    # Find center of track and draw center line and X on center line
    global line_gap
    line_gap = width // 2 if line_gap is None else line_gap
    center_x = None
    center_y = None
    try :
        center_x = int(mean([left_center[0], right_center[0]]))
        center_y = int(mean([left_center[1], right_center[1]]))
        line_gap = right_center[0] - center_x
    except :
        try :
            center_x = right_center[0] - line_gap
            center_y = right_center[1]
        except :
            try :
                center_x = left_center[0] + line_gap
                center_y = left_center[1]
            except :
                pass
    
    if center_x is not None and center_y is not None:
        cv2.line(frame, (center_x + 8, center_y + 8), (center_x - 8, center_y - 8), (0, 0, 255), 2)
        cv2.line(frame, (center_x + 8, center_y - 8), (center_x - 8, center_y + 8), (0, 0, 255), 2)
        cv2.line(frame, (center_x, roi_up), (center_x, roi_down), (255, 255, 0), 2)
    
    # Ordering based on center_x
    movement_order = None
    try :
        if left_edge < center_x < right_edge:
            movement_order = "Go forward"

        elif center_x <= left_edge:
            movement_order = "Turn left"

        elif center_x >= right_edge:
            movement_order = "Turn right"

        # Show and send csv type data to arduino
        cv2.putText(frame, movement_order, (0, (roi_up) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
    except :
        pass
    
    return frame, movement_order