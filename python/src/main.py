# Import libraries
from unittest import result
import cv2

# Import modules
# # import mod.order_sender as sender
import mod.line_detection as line
import mod.crosswalk_detection as crosswalk
import mod.apriltag_detection as apriltag
    
# Capture video from the camera (you might need to adjust the camera index)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        print(FileNotFoundError)
        break
    
    # Detect the april tags
    result_frame, apriltag_order = apriltag.apriltag_detection(frame)
    
    # Detect the croswalk
    result_frame, crosswalk_order = crosswalk.crosswalk_detection(frame)
    
    # Detect the track and lines
    result_frame, line_order = line.line_detection(frame)
    
    # Send order to arduino
    # Sender.order_sender(order)
    
    # Display the frames
    cv2.imshow('Line Detection', result_frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()