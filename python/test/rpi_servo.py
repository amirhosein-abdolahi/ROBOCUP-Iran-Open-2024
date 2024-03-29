from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep

factory = PiGPIOFactory()
servox = AngularServo(18, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=factory)
servoy = AngularServo(17, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=factory)

while True:
    servox.angle = -10
    servoy.angle = 20
    sleep(2)
    servox.angle = -30
    sleep(2)
    servox.angle = -10
    sleep(2)
    servoy.angle = -10
    sleep(2)
