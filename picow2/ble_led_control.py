from machine import Pin
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

# Setup onboard LED
led = Pin("LED", Pin.OUT)

# Initialize BLE peripheral
ble = bluetooth.BLE()
peripheral = BLESimplePeripheral(ble, name="PicoW")

# Define writable characteristic callback
def on_rx(data):
    cmd = data.decode("utf-8").strip().lower()
    print("Received via BLE:", cmd)
    if cmd == "on":
        led.value(1)
    elif cmd == "off":
        led.value(0)

peripheral.on_write(on_rx)

# Main loop
while True:
    if peripheral.is_connected():
        pass  # Do nothing — waiting for data
