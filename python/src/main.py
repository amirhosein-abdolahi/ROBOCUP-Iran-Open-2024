# Import libraries
import cv2


# Import modules
import mod.order_sender as sender
import mod.edge_detection as edge
    
# Capture video from the camera (you might need to adjust the camera index)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        print(FileNotFoundError)
        break
    
    # Detect and track lines with edges
    result_frame, edge_order = edge.edge_detection(frame)
    
    # Send order to arduino
    sender.order_sender(edge_order)
    
    # Display the frames
    cv2.imshow('result', result_frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()