import cv2
import numpy as np

# Method 5: Capture Images or Video
cap = cv2.VideoCapture(0)  # Assuming the camera is connected to the Raspberry Pi

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # :D
    order = "no traffic light"
    
    # :D
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    
    # :D
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([110, 60, 138])
    upper_red = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # :D
    kernel = np.ones((15, 15), "uint8")
    dilate_mask = cv2.dilate(mask, kernel)
    
    # :D
    led_contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    traffic_contours, _ = cv2.findContours(dilate_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # :D
    biger_area = 0
    trafic_x, trafic_y, trafic_w, trafic_h= 0, 0, 0, 0
    for contour in traffic_contours:
        area = cv2.contourArea(contour)
        if (2000 < area < 6000) and (area >= biger_area):
            biger_area = area
            x, y, w, h = cv2.boundingRect(contour)
            trafic_x, trafic_y, trafic_w, trafic_h= x, y, w, h
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
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
                    if y1 <= cy <= y2:
                        order = "yellow light"
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    if y2 < cy < trafic_y + trafic_h:
                        order = "green light"
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        
    
    

    # Display the result
    cv2.imshow('Thresholded', thresholded)
    cv2.imshow('Dilate', dilate_mask)
    cv2.imshow('orginal', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
