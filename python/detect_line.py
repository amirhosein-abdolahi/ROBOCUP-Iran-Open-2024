import cv2
import numpy as np
from statistics import mean
import time
import serial

# Gap size between one line and center
line_gap = None

# Set up the serial connection to arduino
ser = serial.Serial('COM10', 9600)

# Send csv type data to Arduino
def sender(value):
    ser.write(f'{value}\n'.encode())
    time.sleep(0.01)
    # print(value)


# Capture video from the camera (you might need to adjust the camera index)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help with edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Define a region of interest (ROI) to focus on the lanes
    height, width = blurred.shape
    roi_up = (height // 3) * 2
    roi_vertices = [(0, height), (0, roi_up) ,(width, roi_up), (width, height)]
    roi_array_vertices = [np.array(roi_vertices, np.int32)]
    roi_mask = np.zeros_like(blurred)
    cv2.fillPoly(roi_mask, roi_array_vertices, 255)
    roi = cv2.bitwise_and(blurred, roi_mask)

    # Draw the ROI
    cv2.polylines(frame, roi_array_vertices, True, (255, 0, 0), 2)

    # Draw two edge lines
    left_edge = (width // 2) - 20
    right_edge = (width // 2) + 20
    cv2.line(frame, (left_edge, roi_up), (left_edge, height), (255, 0, 255), 2)
    cv2.line(frame, (right_edge, roi_up), (right_edge, height), (255, 0, 255), 2)

    # Thresholding to create a binary image
    _, binary = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area (adjust the threshold as needed)
    min_contour_area = 500
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

    # Draw contours on the original frame
    cv2.drawContours(frame, valid_contours, -1, (0, 255, 0), 2)

    # Find the contour's center
    right_centers = [[], []]
    left_centers = [[], []]
    for contour in valid_contours:
        m = cv2.moments(contour)
        cx = int(m['m10'] / m['m00'])
        cy = int(m['m01'] / m['m00'])
        cv2.line(frame, (cx, cy + 8), (cx, cy - 8), (0, 0, 255), 2)
        cv2.line(frame, (cx + 8, cy), (cx - 8, cy), (0, 0, 255), 2)

        # Clustering center of contours to left and right side
        if cx < width / 2:
            left_centers[0].append(cx)
            left_centers[1].append(cy)

        elif cx > width / 2:
            right_centers[0].append(cx)
            right_centers[1].append(cy)

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
    line_gap = width // 2 if line_gap is None else line_gap
    center_x = None
    center_y = None
    try :
        center_x = int(mean([left_center[0], right_center[0]]))
        center_y = int(mean([left_center[1], right_center[1]]))
        cv2.line(frame, (center_x + 8, center_y + 8), (center_x - 8, center_y - 8), (0, 0, 255), 2)
        cv2.line(frame, (center_x + 8, center_y - 8), (center_x - 8, center_y + 8), (0, 0, 255), 2)
        cv2.line(frame, (center_x, roi_up), (center_x, height), (255, 255, 0), 2)
        line_gap = right_center[0] - center_x
    except :
        try :
            center_x = right_center[0] - line_gap
            center_y = right_center[1]
            cv2.line(frame, (center_x + 8, center_y + 8), (center_x - 8, center_y - 8), (0, 0, 255), 2)
            cv2.line(frame, (center_x + 8, center_y - 8), (center_x - 8, center_y + 8), (0, 0, 255), 2)
            cv2.line(frame, (center_x, roi_up), (center_x, height), (255, 255, 0), 2)
        except :
            try :
                center_x = left_center[0] + line_gap
                center_y = left_center[1]
                cv2.line(frame, (center_x + 8, center_y + 8), (center_x - 8, center_y - 8), (0, 0, 255), 2)
                cv2.line(frame, (center_x + 8, center_y - 8), (center_x - 8, center_y + 8), (0, 0, 255), 2)
                cv2.line(frame, (center_x, roi_up), (center_x, height), (255, 255, 0), 2)
            except :
                pass

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
        sender(movement_order)

    except :
        pass

    # Display the frames
    cv2.imshow('Line Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()
