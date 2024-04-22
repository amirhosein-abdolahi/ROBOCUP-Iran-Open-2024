# Import libraries
import cv2
import numpy as np

# :D
from mod import region_of_interest as ROI

# Function for detect traffic lights
def trafficlight_detection(frame):
    order = 'no light'

    # :D
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # :D
    roi_up = 220
    roi_down = 320
    roi_left = 250
    roi_right = 450
    roi_vertices = [(roi_left, roi_down), (roi_left, roi_up), (roi_right, roi_up), (roi_right, roi_down)]
    roi, frame = ROI.region_of_interest(hsv, frame, roi_vertices)
    
    # :D
    lower_red = np.array([0, 144, 179]) 
    upper_red = np.array([179, 255, 255])
    lower_green = np.array([58, 97, 135])
    upper_green = np.array([179, 255, 255])
    mask_red = cv2.inRange(roi, lower_red, upper_red)
    mask_green = cv2.inRange(roi, lower_green, upper_green)
    
    # :D
    kernel = np.ones((5, 5), "uint8")
    dilate_mask_red = cv2.dilate(mask_red, kernel)
    dilate_mask_green = cv2.dilate(mask_green, kernel)
    
    # :D
    contours_red, _ = cv2.findContours(dilate_mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours_green, _ = cv2.findContours(dilate_mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # :D
    min_area = 500
    valid_contours_red = [cnt for cnt in contours_red if cv2.contourArea(cnt) > min_area]
    valid_contours_green = [cnt for cnt in contours_green if cv2.contourArea(cnt) > min_area]
    
    # :D
    for contour in contours_red:
        x, y, w, h = cv2.boundingRect(contour)
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
    
    for contour in contours_red:
        x, y, w, h = cv2.boundingRect(contour)
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
       
    
    # :D
    if len(valid_contours_green) > 0:
        order = "green light"
    elif len(valid_contours_red) > 0:
        order = "red light"

    return order