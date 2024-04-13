# Import libraries
import cv2
import serial
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo

# Config camera servo motors
factory = PiGPIOFactory()
servox = AngularServo(18, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=factory)
servoy = AngularServo(17, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=factory)
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

# Set the robot mode 
# modes = city, race
mode = 'race'

# Set up the serial connection to arduino
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1) # For raspberry pi '/dev/ttyUSB0'
sleep(5) # Initialized the serial connection

# Define some variables for traffic light
num_light = 0
num_no_light = 100 # Max number of not found light

# Define some variables for parking
sign_to_first = 90
first_to_second = 45
second_to_third = 45

# Set some variables
if mode == 'city':
    best_pos = 40
    normal_pos = 140
elif mode == 'race':
    best_pos = 110
    normal_pos = 190

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

# Main loop
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        print('camera not found')
        break
    
    # Resize the frame
    frame = cv2.resize(frame, (640, 480))
    
    # Detect apriltag
    apriltag_label, apriltag_side = apriltag.apriltag_detection(frame)
    
    # Detect and track lines with edges
    if mode == 'city':
        edge_order = edge.edge_detection(frame, best_pos, normal_pos)
    elif mode == 'race':
        edge_order, xangle = race.detection(frame, servox, xangle)
    
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
        if apriltag_label == 'stop':
            send_order([2, 0, 0, 0, 0])
        else:
            if apriltag_label == 'cross walk':
                go_forward(2)
                send_order([2, 0, 0, 0, 0]) # Stop seconds
                sleep(5)
                go_forward(1)
            elif apriltag_label == 'tunnel beginning':
                send_order([1, 1, 0, 0, steering_order])
            elif apriltag_label == 'tunnel end':
                send_order([1, 2, 0, 0, steering_order])
            elif apriltag_label == 'parking zone':
                
                # Go from sign to first parking zone
                if apriltag_side == 'right':
                    go_forward(4.5)
                elif apriltag_side == 'left':
                    go_forward(8)
                send_order([2, 0, 0, 0, 3]) # Stop seconds
                sleep(1)
                if apriltag_side == 'right':
                    send_order([0, 0, 1, 0, 0]) # Send park order
                elif apriltag_side == 'left':
                    send_order([0, 0, 2, 0, 0]) # Send park order
                sleep(1)
                
                # Go from first to second parking zone
                if apriltag_side == 'right':
                    go_forward(2.25)
                elif apriltag_side == 'left':
                    go_forward(1)
                send_order([2, 0, 0, 0, 3]) # Stop seconds
                sleep(1)
                if apriltag_side == 'right':
                    send_order([0, 0, 1, 0, 0]) # Send park order
                elif apriltag_side == 'left':
                    send_order([0, 0, 2, 0, 0]) # Send park order
                sleep(1)
                
                # Go from second to third parking zone
                if apriltag_side == 'right':
                    go_forward(2.25)
                elif apriltag_side == 'left':
                    go_forward(1)
                send_order([2, 0, 0, 0, 3]) # Stop seconds
                sleep(1)
                if apriltag_side == 'right':
                    send_order([0, 0, 1, 0, 0]) # Send park order
                elif apriltag_side == 'left':
                    send_order([0, 0, 2, 0, 0]) # Send park order
                sleep(1)
            else:
                crosswalk_order = crosswalk.crosswalk_detection(frame) # Detect crosswalk
                if crosswalk_order == 'crosswalk':
                    send_order([2, 0, 0, 0, 3]) # Stop befor the crosswalk
                    servox.angle = -30 # Move camera to detect apriltag
                    sleep(1)
                    while True:
                        _, frame = cap.read()
                        frame = cv2.resize(frame, (640, 480))
                        apriltag_label, apriltag_side = apriltag.apriltag_detection(frame) # Detect apriltag
                        if apriltag_label in intersection_sign:
                            sign_order = intersection_sign.get(apriltag_label)
                            sleep(1)
                            break
                    servox.angle = xangle # Reset camera position
                    servoy.angle = -10 # Move camera to detect traffic light
                    sleep(1)
                    while True:
                        _, frame = cap.read()
                        frame = cv2.resize(frame, (640, 480))
                        trafficlight_order = light.trafficlight_detection(frame) # Detect traffic light
                        print(trafficlight_order) # Debuging
                        print(num_light) # Debuging
                        if trafficlight_order != 'no light':
                            if trafficlight_order == 'green light':
                                servoy.angle = yangle # Reset camera position
                                sleep(1)
                                send_order([1, 0, 0, 0, 3], 4.5) # Go forward for secends
                                send_order([0, 0, 0, sign_order, 0])
                                num_light = 0
                                break
                        elif num_light > num_no_light:
                            servoy.angle = yangle # Reset camera position
                            sleep(1)
                            send_order([1, 0, 0, 0, 3], 4.5) # Go forward for secends
                            send_order([0, 0, 0, sign_order, 0])
                            num_light = 0
                            break
                        else:
                            sleep(0.05)
                            num_light += 1
                else:
                    send_order([1, 0, 0, 0, steering_order]) # Go forward

    elif mode == 'race': # Race mode
        if apriltag_label == 'stop':
            send_order([2, 0, 0, 0, 0])
        else:
            send_order([1, 0, 0, 0, steering_order]) # Go forward

    # Display the frames
    cv2.imshow('result', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()