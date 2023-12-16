import cv2
import serial
import time

# Set up the serial connection to Arduino
ser = serial.Serial('COM7', 9600)

def on_trackbar_change(value):
    ser.write(f'{int(value)}\n'.encode())
    # time.sleep(0.5)
    print(value)

# Create a simple GUI with a trackbar
cv2.namedWindow('Servo Control')
cv2.createTrackbar('Angle', 'Servo Control', 90, 180, on_trackbar_change)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Press 'Esc' to exit
        break

cv2.destroyAllWindows()
ser.close()
