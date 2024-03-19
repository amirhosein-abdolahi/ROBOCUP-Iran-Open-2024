# Import libraries
import cv2
import serial
import time

# Import modules
import mod.edge_detection as edge
import mod.crosswalk_detection as crosswalk
import mod.apriltag_detection as apriltag
import mod.trafficlight_detection as light

# Set up the serial connection to arduino
ser = serial.Serial('COM10', 9600) # For raspberry pi '/dev/ttyUSB0'
time.sleep(5) # Initialized the serial connection

# Function for sending orders to arduino
last_order = None
def send_orders(order):
    if last_order != order:
        last_order = order
        ser.write(order.encode())
        time.sleep(.01)

# Capture video from the camera (you might need to adjust the camera index)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        print(FileNotFoundError)
        break
    
    # Detect apriltag
    result_frame, apriltag_label, apriltag_side = apriltag.apriltag_detection(frame)
    
    # Detect and track lines with edges
    result_frame, edge_order = edge.edge_detection(frame)
    
    # Maping edge order with number
    steering, motor = 0, 0
    if edge_order == 'forward':
        steering, motor = 3, 1
    elif edge_order == 'right':
        steering, motor = 2, 1
    elif edge_order == 'left':
        steering, motor = 4, 1
    elif edge_order == 'right right':
        steering, motor = 1, 1
    elif edge_order == 'left left':
        steering, motor = 5, 1
    else:
        steering, motor = 3, 1
    
    # :D
    crosswalk_order = 'no crosswalk'
    trafficlight_order = 'no light'
    
    # :D
    order = [None for a in range(5)]
    exist_light = 0
    if apriltag_label == 'stop':
        order = [3, 2, 0, 0, 0]
    else:
        if apriltag_label == 'parking zone':
            if apriltag_side == 'right':
                order = [3, 2, 0, 0, 0] # stop
            elif apriltag_side == 'left':
                order = [3, 2, 0, 0, 0] # stop
        else:
            # Detect cross walk
            result_frame, crosswalk_order = crosswalk.crosswalk_detection(frame)
            if crosswalk_order == 'crosswalk':
                # Detect traffic light
                result_frame, trafficlight_order = light.trafficlight_detection(frame)
                if apriltag_label == 'go straight':
                    if trafficlight_order != 'no light':
                        if (trafficlight_order == 'greenlight') or (exist_light >= 300):
                            order = [3, 2, 2, 0, 0]
                            exist_light = 0
                    else:
                        exist_light += 1
                elif apriltag_label == 'turn right':
                    if trafficlight_order != 'no light':
                        if (trafficlight_order == 'greenlight') or (exist_light >= 300):
                            order = [3, 2, 1, 0, 0]
                            exist_light = 0
                    else:
                        exist_light += 1
                elif apriltag_label == 'turn left':
                    if trafficlight_order != 'no light':
                        if (trafficlight_order == 'greenlight') or (exist_light >= 300):
                            order = [3, 2, 3, 0, 0]
                            exist_light = 0
                    else:
                        exist_light += 1
                else:
                    order = [3, 2, 0, 0, 0]
                    time.sleep(3) # Stop 3 seconds before crosswalk
                    order = [steering, motor, 0, 0, 0]
            else:
                order = [steering, motor, 0, 0, 0]

    # Check the tunnel
    if apriltag_label == 'tunnel beginning':
        order[4] = 1
    elif apriltag_label == 'tunnel end':
        order[4] = 2
        
    # Convert list to string
    order = "".join(map(str, order))
    
    # Send order to arduino
    send_orders(order)
    
    # Show order
    text = f"{apriltag_label}\n{crosswalk_order}\n{trafficlight_order}\n{edge_order}\n{order}"
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