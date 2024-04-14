from gpiozero import Button
from signal import pause
import subprocess as sp

# Connect a push button to GPIO pin 3
button = Button(3)

# Initialize extProc as None (global scope)
extProc = None

# Run main program
def start_program():
    global extProc
    extProc = sp.Popen(["python", "src/main.py"])

# Define actions for button press
def action():
    print("Reset button pressed...")

    # Check if extProc is running
    if extProc and extProc.poll() is None:
        # Terminate the program
        extProc.terminate()
        extProc.wait()  # Wait for the process to finish

    # Start the program again
    start_program()

# Assign actions to button events
button.when_pressed = action

# Start the program initially
start_program()

# Keep the script running
pause()
