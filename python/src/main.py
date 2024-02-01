# import libraries
import cv2

# Import modules
import mod.line_detection as line
# import mod.order_sender as sender
    
# Capture video from the camera (you might need to adjust the camera index)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        print(FileNotFoundError)
        break
    
    # detect the track and lines
    frame, order = line.line_detection(frame)
    
    # send order to arduino
    # sender.order_sender(order)
    
    # Display the frames
    cv2.imshow('Line Detection', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()