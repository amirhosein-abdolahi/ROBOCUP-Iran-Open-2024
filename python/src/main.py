# Import libraries
import cv2


# Import modules
import mod.order_sender as sender
import mod.edge_detection as edge
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
    
    # Detect apriltag
    result_frame, apriltag_label = apriltag.apriltag_detection(frame)
    
    # Detect cross walk
    result_frame, crosswalk_order = crosswalk.crosswalk_detection(frame)
    
    # Detect and track lines with edges
    result_frame, edge_order = edge.edge_detection(frame)
    
    # Send order to arduino
    if apriltag_label == "stop":
        order = "stop"  
    else:
        if crosswalk_order == "crosswalk":
            order = "stop"
        else:
            order = edge_order
    
    sender.order_sender(order)
    
    # Show order
    text = f"{apriltag_label}\n{crosswalk_order}\n{edge_order}\n{order}"
    y0, dy = 30, 25
    for i, line in enumerate(text.split('\n')):
        y = y0 + i * dy
        cv2.putText(frame, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (128, 54, 234), 2)
    
    # Display the frames
    cv2.imshow('result', result_frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()