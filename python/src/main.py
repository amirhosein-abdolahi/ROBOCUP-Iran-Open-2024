# Import libraries
import cv2
import serial
import time

# Import modules
import mod.edge_detection as edge
import mod.crosswalk_detection as crosswalk
import mod.apriltag_detection as apriltag
import mod.trafficlight_detection as light

# Set the robot mode 
# modes = city, race
mode = 'city'

# Set up the serial connection to arduino
ser = serial.Serial(port='COM7', baudrate=9600, timeout=.1) # For raspberry pi '/dev/ttyUSB0'
time.sleep(5) # Initialized the serial connection

# Define some variables
exist_light = 0
num_no_light = 300 # Max number of not found light

# Function for sending orders to arduino
def send_order(order, delay=.05):
    
    # Convert list to string
    order = "".join(map(str, order))
    
    # Send order to arduino
    ser.write(order.encode())
    time.sleep(delay)
        
    # Show order
    if mode == 'city':
        text = f"{mode}\n{apriltag_label}\n{crosswalk_order}\n{trafficlight_order}\n{edge_order}\n{order}"
    elif mode == 'race':
        text = f"{mode}\n{apriltag_label}\n{edge_order}\n{order}"
    y0, dy = 30, 25
    for i, line in enumerate(text.split('\n')):
        y = y0 + i * dy
        cv2.putText(frame, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, .8, (128, 54, 234), 2)
        
# Capture video from the camera (you might need to adjust the camera index)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        print('camera not found')
        break
    
    # Resize the frame
    frame = cv2.resize(frame, (480, 360))
    
    # Detect apriltag
    result_frame, apriltag_label, apriltag_side = apriltag.apriltag_detection(frame)
    
    # Detect and track lines with edges
    result_frame, edge_order = edge.edge_detection(frame)
    
    # Maping edge order with number
    steering = 0
    if edge_order == 'forward':
        steering = 3
    elif edge_order == 'right':
        steering = 4
    elif edge_order == 'left':
        steering = 2
    elif edge_order == 'right right':
        steering = 5
    elif edge_order == 'left left':
        steering = 1
    else:
        steering = 3
    
    # Set default of some values
    crosswalk_order = 'no crosswalk'
    trafficlight_order = 'no light'
    
    # Find the order
    if mode == 'city': # City mode
        if apriltag_label == 'stop':
            send_order([2, 0, 0, 0, 0])
        else:
            if apriltag_label == 'parking zone':
                if apriltag_side == 'right':
                    send_order([0, 0, 1, 0, 0])
                elif apriltag_side == 'left':
                    send_order([0, 0, 2, 0, 0])
            elif apriltag_side == 'tunnel beginning':
                send_order([0, 1, 0, 0, 0])
                send_order([1, 0, 0, 0, 3], 1) # Go forward 1 second to skip apriltag
            elif apriltag_label == 'tunnel end':
                send_order([0, 2, 0, 0, 0])
                send_order([1, 0, 0, 0, 3], 1) # Go forward 1 second to skip apriltag
            else:
                # Detect crosswalk
                result_frame, crosswalk_order = crosswalk.crosswalk_detection(frame)
                if crosswalk_order == 'crosswalk':
                    # Detect traffic light
                    result_frame, trafficlight_order = light.trafficlight_detection(frame)
                    if apriltag_label == 'go straight':
                        if trafficlight_order != 'no light':
                            if (trafficlight_order == 'greenlight') or (exist_light >= num_no_light):
                                send_order([0, 0, 0, 2, 0])
                            exist_light = 0
                        else:
                            exist_light += 1
                    elif apriltag_label == 'turn right':
                        if trafficlight_order != 'no light':
                            if (trafficlight_order == 'greenlight') or (exist_light >= num_no_light):
                                send_order([0, 0, 0, 1, 0])
                            exist_light = 0
                        else:
                            exist_light += 1
                    elif apriltag_label == 'turn left':
                        if trafficlight_order != 'no light':
                            if (trafficlight_order == 'greenlight') or (exist_light >= num_no_light):
                                send_order([0, 0, 0, 3, 0])
                            exist_light = 0
                        else:
                            exist_light += 1
                    else:
                        send_order([2, 0, 0, 0, 0], 5) # Stop 5 seconds before crosswalk
                        send_order([1, 0, 0, 0, 3], 3) # Go forward for 3 seconds to skip crosswalk
                else:
                    send_order([1, 0, 0, 0, steering]) # Go forward

    elif mode == 'race': # Race mode
        if apriltag_label == 'stop':
            send_order([2, 0, 0, 0, 0])
        else:
            send_order([1, 0, 0, 0, steering]) # Go forward

    # Display the frames
    cv2.imshow('result', result_frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()