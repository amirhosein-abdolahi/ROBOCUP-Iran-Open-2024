# Import libraries
import cv2
import numpy as np

# Function for detect traffic lights
def trafficlight_detection(frame):
    order = 'no traffic light'
    
    # Change frame color type and threshold for find lights
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    
    # Change frame color type and color detection for find traffic light
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([100, 80, 70])
    upper_red = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Morphological Transform, Dilation 
    kernel = np.ones((15, 15), "uint8")
    dilate_mask = cv2.dilate(mask, kernel)
    
    # Find contours
    led_contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    traffic_contours, _ = cv2.findContours(dilate_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # Find traffic light
    biger_area = 0
    global trafic_x, trafic_y, trafic_w, trafic_h
    trafic_x, trafic_y, trafic_w, trafic_h= 0, 0, 0, 0
    for contour in traffic_contours:
        area = cv2.contourArea(contour)
        if (2000 < area < 4000) and (area >= biger_area):
            biger_area = area
            x, y, w, h = cv2.boundingRect(contour)
            trafic_x, trafic_y, trafic_w, trafic_h= x, y, w, h
            cv2.rectangle(frame, (x, y), (x + w, y + h), (240, 130, 50), 2)
    
    # Find lights and issue the order
    for contour in led_contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        if 30 < area < 300:
            if trafic_x < x < trafic_x + trafic_w:
                if trafic_y < y < trafic_y + trafic_h:
                    y1 = trafic_y + trafic_h / 3
                    y2 = y1 + trafic_h / 3
                    
                    M = cv2.moments(contour)
                    cy = int(M['m01']/M['m00'])
                                        
                    if trafic_y < cy < y1:
                        order = "red light"
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    elif y1 <= cy <= y2:
                        order = "yellow light"
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    elif y2 < cy < trafic_y + trafic_h:
                        order = "green light"
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    else:
                        order = "no light"
            else:
                order = "no light"
        else:
            order = "no light"
    return frame, order