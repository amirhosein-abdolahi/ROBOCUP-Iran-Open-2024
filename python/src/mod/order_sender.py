# Import the libraries
import serial
import time

# Set up the serial connection to arduino
ser = serial.Serial('COM10', 9600) # For raspberry pi '/dev/ttyUSB0'
time.sleep(5) # Initialized the serial connection

# Send csv type data to Arduino
def order_sender(value):
    if value == "Go forward":
        ser.write("center,forward\n".encode())
    elif value == "Turn left":
        ser.write("left,forward\n".encode())
    elif value == "Turn right":
        ser.write("right,forward\n".encode())
    time.sleep(0.01)