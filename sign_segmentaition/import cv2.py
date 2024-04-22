import cv2
import numpy as np
import os
# Load the template image
right = cv2.imread('C:/Users/amhab/Desktop/right.jpg', 0)
left = cv2.imread('C:/Users/amhab/Desktop/left.jpg', 0)

cap = cv2.VideoCapture(0)  # Open the webcam (0 for default webcam)

# Define scale factors and rotation angles
signs = [right, left]
scales = [1.0]
angles = [-5, 0, 5]

while True:
    ret, frame = cap.read()  # Read a frame from the webcam

	# Convert the frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Iterate over different scales and rotations
    for sign in signs:
        for scale in scales:
            for angle in angles:
                # Apply scale and rotation to the template image
                template_resized = cv2.resize(sign, None, fx=scale, fy=scale)
                rows, cols = template_resized.shape
                M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
                template_rotated = cv2.warpAffine(template_resized, M, (cols, rows))

                # Perform template matching
                res = cv2.matchTemplate(frame_gray, template_rotated, cv2.TM_CCOEFF_NORMED)
                threshold = 0.6
                loc = np.where(res >= threshold)

                # Draw rectangles around the matched templates
                w, h = template_rotated.shape[::-1]
                for pt in zip(*loc[::-1]):
                    bottom_right = (pt[0] + int(w), pt[1] + int(h))
                    cv2.rectangle(frame, pt, bottom_right, (0, 255, 0), 2)
                    # cv2.putText(frame, sign.split('/'), bottom_right, 2, (255, 0, 0), 2)
                    cv2.putText(frame, str(sign), bottom_right, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)

	# Display the result
    cv2.imshow('Live Template Matching', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit the loop
    	break

cap.release()  # Release the webcam
cv2.destroyAllWindows()
