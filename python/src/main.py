# Import libraries
import cv2
import numpy as np
import serial
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo

# Set the robot mode 
# modes = city, race
mode = 'city'
edge_order = 'forward'

# Config camera servo motors
factory = PiGPIOFactory()
servox = AngularServo(18, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=factory)
servoy = AngularServo(17, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=factory)
if mode == 'city':
    xangle = -10
    yangle = 10
elif mode == 'race':
    xangle = -10
    yangle = 20
servox.angle = xangle
servoy.angle = yangle

# Import modules
import mod.edge_detection as edge
import mod.crosswalk_detection as crosswalk
import mod.apriltag_detection as apriltag
import mod.trafficlight_detection as light
import mod.edge_detection_race as race

# Set up the serial connection to arduino
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1) # For raspberry pi '/dev/ttyUSB0'
sleep(5) # Initialized the serial connection

# Define some variables for stop sign
num_stop_sign = 0
num_no_stop_sign = 80

# Define some variables for traffic light
num_light = 0
num_no_light = 10 # Max number of not found light

# Define some variables for sign
num_sign = 0
num_no_sign = 100 # Max number of not found sign

# # Define some variables for parking
# sign_to_first = 90
# first_to_second = 45
# second_to_third = 45

# Set some variables
if mode == 'city':
    best_pos = 30
    normal_pos = 130
elif mode == 'race':
    best_pos = 130
    normal_pos = 180
    
# Function for sending orders to arduino
def send_order(order, delay=0.05):
    
    # Convert list to string
    order = "".join(map(str, order))
    
    # Send order to arduino
    ser.write(order.encode())
    sleep(delay)
        
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
# cap_park = cv2.VideoCapture(2)

# Function for go forward with edge detection
def go_forward(time):
    delay_time = 0
    while delay_time < (time * 20):
        _, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        edge_order = edge.edge_detection(frame, best_pos, normal_pos) # Detete edge
        if edge_order in steering:
            steering_order = steering.get(edge_order)
            send_order([1, 0, 0, 0, steering_order]) # Go foward
        delay_time += 1
        
        # Show frame
        cv2.putText(frame, "GO FORWARD", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (128, 54, 234), 5)
        # cv2.imshow('result', frame)
        cv2.waitKey(1)
        
# Main loop
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    # ret_park, frame_park = cap_park.read()
    if not ret:
        print('camera not found')
        break
    
    # Resize the frame
    frame = cv2.resize(frame, (640, 480))
    # frame_park = cv2.resize(frame_park, (640, 480))
    # frame_park = cv2.rotate(frame_park, cv2.ROTATE_90_CLOCKWISE)
    
    # # Detect apriltag from park camera
    # apriltag_label_park = apriltag.apriltag_detection(frame_park, 150)
    
    # Detect apriltag
    if mode == 'city':
        apriltag_label = apriltag.apriltag_detection(frame, 150)
    elif mode == 'race':
        apriltag_label = apriltag.apriltag_detection(frame, 250)
        
    
    # Detect and track lines with edges
    if mode == 'city':
        edge_order = edge.edge_detection(frame, best_pos, normal_pos)
    elif mode == 'race':
        edge_order = race.detection(frame, best_pos, normal_pos, edge_order)
    
    # Maping edge order with number
    steering = {
        'forward': 3,
        'right': 4,
        'left': 2,
        'right right': 5,
        'left left': 1
    }
    steering_order = 3
    if edge_order in steering:
        steering_order = steering.get(edge_order)
        
    # Mapping intersection sign
    sign_order = 0
    intersection_sign = {
        'go straight': 2,
        'turn right': 1,
        'turn left': 3
    }
        
    # Set default of some values
    crosswalk_order = 'no crosswalk'
    trafficlight_order = 'no light'
    
    # Find the order
    if mode == 'city': # City mode

        # Check state of robot
        if apriltag_label == 'stop':
            send_order([2, 0, 0, 0, 0])
            num_stop_sign = 0
        else:
            if num_stop_sign < num_no_stop_sign:
                send_order([2, 0, 0, 0, 0])
                num_stop_sign += 1
                sleep(0.05) 
            elif apriltag_label == 'cross walk':
                go_forward(2)
                send_order([2, 0, 0, 0, 0]) # Stop seconds
                sleep(5)
                go_forward(1)
            elif apriltag_label == 'tunnel beginning':
                send_order([1, 1, 0, 0, steering_order])
            elif apriltag_label == 'tunnel end':
                send_order([1, 2, 0, 0, steering_order])
            # elif apriltag_label == 'parking zone':
            #     # Go from sign to first parking zone
            #     go_forward(4.5)
            #     send_order([2, 0, 0, 0, 3]) # Stop seconds
            #     sleep(1)
            #     send_order([0, 0, 1, 0, 0]) # Send park order
            #     sleep(1)
                
            #     # Go from first to second parking zone
            #     go_forward(2.25)
            #     send_order([2, 0, 0, 0, 3]) # Stop seconds
            #     sleep(1)
            #     send_order([0, 0, 1, 0, 0]) # Send park order
            #     sleep(1)
                
            #     # Go from second to third parking zone
            #     go_forward(2.25)
            #     send_order([2, 0, 0, 0, 3]) # Stop seconds
            #     sleep(1)
            #     send_order([0, 0, 1, 0, 0]) # Send park order
            #     sleep(1)
            # elif apriltag_label_park == 'parking zone':
            #     # Go from sign to first parking zone
            #     go_forward(4.5)
            #     send_order([2, 0, 0, 0, 3]) # Stop seconds
            #     sleep(1)
            #     send_order([0, 0, 1, 0, 0]) # Send park order
            #     sleep(1)
                
            #     # Go from first to second parking zone
            #     go_forward(2.25)
            #     send_order([2, 0, 0, 0, 3]) # Stop seconds
            #     sleep(1)
            #     send_order([0, 0, 1, 0, 0]) # Send park order
            #     sleep(1)
                
            #     # Go from second to third parking zone
            #     go_forward(2.25)
            #     send_order([2, 0, 0, 0, 3]) # Stop seconds
            #     sleep(1)
            #     send_order([0, 0, 1, 0, 0]) # Send park order
            #     sleep(1)
            else:
                crosswalk_order = crosswalk.crosswalk_detection(frame) # Detect crosswalk
                if crosswalk_order == 'crosswalk':
                    send_order([2, 0, 0, 0, 3]) # Stop befor the crosswalk
                    sleep(1)
                    servox.angle = -45 # Move camera to detect apriltag
                    sleep(1)
                    while True:
                        _, frame = cap.read()
                        frame = cv2.resize(frame, (640, 480))
                        apriltag_label = apriltag.apriltag_detection(frame, 150) # Detect apriltag
                        print(apriltag_label) # Debuging
                        print(num_sign) # Debuging
                        if apriltag_label in intersection_sign:
                            sign_order = intersection_sign.get(apriltag_label)
                            num_sign = 0
                            sleep(1)
                            break
                        elif num_sign > num_no_sign:
                            sign_order = 2 # Go straight
                            num_sign = 0
                            sleep(1)
                            break
                        else:
                            sleep(0.05)
                            num_sign += 1
                        # Show frame
                        cv2.putText(frame, "SIGN CHECK", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (128, 54, 234), 5)
                        # cv2.imshow('result', frame)
                        cv2.waitKey(1)
                    servox.angle = xangle # Reset camera position
                    # servoy.angle = -10 # Move camera to detect traffic light
                    sleep(1)
                    while True:
                        _, frame = cap.read()
                        frame = cv2.resize(frame, (640, 480))
                        trafficlight_order = light.trafficlight_detection(frame) # Detect traffic light
                        print(trafficlight_order) # Debuging
                        print(num_light) # Debuging
                        if trafficlight_order != 'no light':
                            if trafficlight_order == 'green light':
                                # servoy.angle = yangle # Reset camera position
                                # sleep(1)
                                # send_order([1, 0, 0, 0, 3], 4.5) # Go forward for secends
                                send_order([0, 0, 0, sign_order, 0])
                                sleep(17)
                                num_light = 0
                                break
                        elif num_light > num_no_light:
                            # servoy.angle = yangle # Reset camera position
                            # sleep(1)
                            # send_order([1, 0, 0, 0, 3], 4.5) # Go forward for secends
                            send_order([0, 0, 0, sign_order, 0])
                            sleep(17)
                            num_light = 0
                            break
                        else:
                            sleep(0.05)
                            num_light += 1
                        # Show frame
                        cv2.putText(frame, "LIGHT CHECK", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (128, 54, 234), 5)
                        # cv2.imshow('result', frame)
                        cv2.waitKey(1)
                else:
                    send_order([1, 0, 0, 0, steering_order]) # Go forward
        
        # # Display the park frame
        # cv2.imshow('park frame', frame_park)
                    
    elif mode == 'race': # Race mode
        if apriltag_label == 'stop':
            send_order([2, 0, 0, 0, 0])
            num_stop_sign = 0
        elif num_stop_sign < num_no_stop_sign:
            send_order([2, 0, 0, 0, 0])
            num_stop_sign += 1
            sleep(0.05)
        else:
            send_order([1, 0, 0, 0, steering_order]) # Go forward
            
    # Display the frames
    # cv2.imshow('result', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# Release the video capture object and close windows
cap.release()
# cap_park.release()
cv2.destroyAllWindows()
