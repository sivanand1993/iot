from time import sleep
from machine import Pin

led=Pin("LED",Pin.OUT)
while True:
    led.toggle()
    sleep(2)
    led.toggle()
    sleep(1)
    led.toggle()
    sleep(0.5)