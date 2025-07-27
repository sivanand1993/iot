from time import sleep
from machine import Pin
from machine import ADC
from machine import PWM

led=PWM(Pin(15,Pin.OUT))
led.freq(1000)
potentiometer=ADC(26)


while True:
    led.duty_u16(potentiometer.read_u16())

    
    