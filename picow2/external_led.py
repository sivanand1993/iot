from time import sleep
from machine import Pin

led=Pin(15,Pin.OUT)
button=Pin(15,Pin.IN)
while True:
    if button.value()==1:
        led.on()
        sleep(2)
led.off()