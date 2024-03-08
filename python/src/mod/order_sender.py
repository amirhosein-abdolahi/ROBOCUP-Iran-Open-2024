# Import the libraries
import serial
import time

# Set up the serial connection to arduino
ser = serial.Serial('COM10', 9600) # For raspberry pi '/dev/ttyUSB0'
time.sleep(5) # Initialized the serial connection

# Send csv type data to Arduino
def order_sender(value):
    global order
    if value == "stop":
        order = "center,stop\n"
        
    elif value == "forward":
        order = "center,forward\n"
        
    elif value == "right":
        order = "right,forward\n"
        
    elif value == "left":
        order = "left,forward\n"
    
    elif value == "right right":
        order = "right_right,forward\n"
        
    elif value == "left left":
        order = "left_left,forward\n"
    
    elif value == "no line":
        order = "center,forward\n"
    
    else:
        order = "center,stop\n"
    
    ser.write(order.encode())
        
    time.sleep(0.01)