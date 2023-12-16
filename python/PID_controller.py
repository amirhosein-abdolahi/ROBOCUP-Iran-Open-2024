import cv2
import numpy as np

# PID controller parameters (adjust as needed)
Kp = 0.1  # Proportional gain
Ki = 0.01  # Integral gain
Kd = 0.05  # Derivative gain

# Setpoint (desired position between the lines)
setpoint = 320  # Adjust based on the image size

# Initialize PID controller variables
integral = 0
previous_error = 0

# Capture video from the camera (you might need to adjust the camera index)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Thresholding to create a binary image
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area (adjust the threshold as needed)
    min_contour_area = 500
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

    # Calculate the centroid of the valid contours
    if valid_contours:
        largest_contour = max(valid_contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M["m01"] / M["m00"])

        # PID control
        error = cx - setpoint
        integral += error
        derivative = error - previous_error
        output = Kp * error + Ki * integral + Kd * derivative

        # Move the robot based on the PID output (adjust as needed)
        # For simplicity, assume a linear relationship between output and robot movement
        # You may need to convert this to control signals suitable for your robot's actuators.
        move_command = 0.5 * output  # Adjust the scaling factor based on your robot's characteristics

        # Print the PID components for debugging
        print(f"P: {int(Kp * error)}, I: {int(Ki * integral)}, D: {int(Kd * derivative)}")

        # Display the frames
        cv2.line(frame, (setpoint, 0), (setpoint, frame.shape[0]), (0, 255, 0), 2)  # Draw the setpoint line
        cv2.drawContours(frame, valid_contours, -1, (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), 2) # Draw the center
        cv2.imshow('Robot Control', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()
