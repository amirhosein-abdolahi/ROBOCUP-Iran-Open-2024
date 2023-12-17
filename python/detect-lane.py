import cv2
import numpy as np

def detect_lanes(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help with edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection using Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Define a region of interest (ROI) to focus on the lanes
    height, width = edges.shape
    roi_vertices = [(0, height), (width / 2, height / 2), (width, height)]
    roi_mask = np.zeros_like(edges)
    cv2.fillPoly(roi_mask, [np.array(roi_vertices, np.int32)], 255)
    roi = cv2.bitwise_and(edges, roi_mask)

    # Use HoughLines to detect lines in the image
    lines = cv2.HoughLinesP(roi, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=30)

    # Draw the detected lines on the original image
    result = np.copy(image)
    draw_lines(result, lines)

    return result

def draw_lines(image, lines):
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Open a video capture object (0 for default camera, adjust as needed)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        break

    # Detect lanes in the frame
    output_frame = detect_lanes(frame)

    # Display the result in a window
    cv2.imshow('Lane Detection', output_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
