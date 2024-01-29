import customtkinter
import serial
import time

# Set up the serial connection to arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)

# functions for send order
value1 = "center"
value2 = "stop"

def send_value():
    ser.write(f"{value1},{value2}\n".encode())
    time.sleep(0.01)
    print(f"({value1} , {value2})")

def forward():
    # print("forward")
    global value2
    value2 = "forward"
    send_value()

def backward():
    # print("backward")
    global value2
    value2 = "backward"
    send_value()

def turn_left():
    # print("turn_left")
    global value1
    value1 = "left"
    send_value()

def turn_right():
    # print("turn_right")
    global value1
    value1 = "right"
    send_value()

def stop():
    # print("stop")
    global value2
    value2 = "stop"
    send_value()

def center():
    # print("center")
    global value1
    value1 = "center"
    send_value()

# System settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Our app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Application")

# Add label
lable = customtkinter.CTkLabel(app, text="Controller Robot", font=("", 30))
lable.grid(column=0, row=0, padx=10, pady=10, columnspan=3)

# Add control buttons
forwardBut = customtkinter.CTkButton(app,
                                  text="↑",
                                  width=100,
                                  height=100,
                                  font=("", 70),
                                  command=forward)

turn_rightBut = customtkinter.CTkButton(app,
                                  text="→",
                                  width=100,
                                  height=100,
                                  font=("", 70),
                                  command=turn_right)

backwardBut = customtkinter.CTkButton(app,
                                  text="↓",
                                  width=100,
                                  height=100,
                                  font=("", 70),
                                  command=backward)

turn_leftBut = customtkinter.CTkButton(app,
                                  text="←",
                                  width=100,
                                  height=100,
                                  font=("", 70),
                                  command=turn_left)

stopBut = customtkinter.CTkButton(app,
                                  text="▢",
                                  width=100,
                                  height=100,
                                  font=("", 70),
                                  command=stop)

centerBut = customtkinter.CTkButton(app,
                                  text="▢",
                                  width=100,
                                  height=100,
                                  font=("", 70),
                                  command=center)

forwardBut.grid(column=3, row=1, padx= 100, pady=10)
turn_leftBut.grid(column=0, row=2, padx=10, pady=10, sticky="e")
stopBut.grid(column=3, row=2, padx=10, pady=10)
turn_rightBut.grid(column=2, row=2, padx=10, pady=10, sticky="w")
backwardBut.grid(column=3, row=3, padx=10, pady=10)
centerBut.grid(column=1, row=2, padx=10, pady=10)

# Run the application
app.mainloop()
