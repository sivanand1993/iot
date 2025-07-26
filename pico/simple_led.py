from time import sleep
from machine import Pin

led=Pin("LED",Pin.OUT)
while True:
    led.toggle()
    sleep(0.1)