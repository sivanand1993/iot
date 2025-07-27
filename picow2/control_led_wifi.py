import network
import socket
from time import sleep
import machine

from machine import Pin,
led=Pin("LED",Pin.OUT)

ssid = 'Soumith'
password = 'Xfinity!23'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    wlan.ifconfig(('10.0.0.181', '255.255.255.0', '10.0.0.181', '8.8.8.8'))#made up ip address
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <form action="./turnoff">
            <input type="submit" value="Reprogramme" />
            </form>
            <p>LED is {state}</p>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start a web server
    state = 'OFF'
    led.off()
    request=None
    
    while request !='/turnoff?':
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            led.on()
            state = 'ON'
        elif request =='/lightoff?':
            led.off()
            state = 'OFF'
        html = webpage(state)
        client.send(html)
        client.close()
    
try:
    ip=connect()
    led.on()
    sleep(3)
    led.off()
    connection=open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
    

led.on()
sleep(2)
led.off()