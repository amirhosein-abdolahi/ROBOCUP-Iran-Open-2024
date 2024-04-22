# Import libraries
import cv2
# Import modules
import mod.trafficlight_detection as light

# Capture video from the camera (you might need to adjust the camera index)
cap = cv2.VideoCapture(0)

# Main loop
while True:
    _, frame = cap.read()
    
    # Resize the frame
    frame = cv2.resize(frame, (640, 480))
    
    # Detect traffic light
    order = light.trafficlight_detection(frame)
    
    # Display the frames
    cv2.imshow('result', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()