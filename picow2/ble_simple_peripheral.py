import bluetooth
import struct
from ble_advertising import advertising_payload
from micropython import const

# IRQ event constants (use integers directly)
_IRQ_CENTRAL_CONNECT = 1
_IRQ_CENTRAL_DISCONNECT = 2
_IRQ_GATTS_WRITE = 3

# Nordic UART Service UUIDs
_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")

# Characteristic flags
_FLAG_READ = const(0x0002)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)

class BLESimplePeripheral:
    def __init__(self, ble, name="PicoW"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)

        self._connections = set()
        self._rx_handler = None

        # Define characteristics
        self._tx_char = (_UART_TX_CHAR_UUID, _FLAG_NOTIFY)
        self._rx_char = (_UART_RX_CHAR_UUID, _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE)

        # Register service
        self._service = (_UART_SERVICE_UUID, (self._tx_char, self._rx_char))
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((self._service,))

        # Advertise
        self._payload = advertising_payload(name=name, services=[_UART_SERVICE_UUID])
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("Connected:", conn_handle)

        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.discard(conn_handle)
            print("Disconnected:", conn_handle)
            self._advertise()

        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            if value_handle == self._rx_handle:
                value = self._ble.gatts_read(self._rx_handle)
                if self._rx_handler:
                    self._rx_handler(value)

    def on_write(self, handler):
        self._rx_handler = handler

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def is_connected(self):
        return bool(self._connections)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
