import struct

# BLE advertisement types
_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x03)
_ADV_TYPE_UUID32_COMPLETE = const(0x05)
_ADV_TYPE_UUID128_COMPLETE = const(0x07)

# BLE flags
_ADV_FLAG_GENERAL_DISC = 0x02
_ADV_FLAG_NO_BREDR = 0x04

def advertising_payload(limited_disc=False, br_edr=False, name=None, services=None):
    payload = bytearray()

    # Flags
    flags = (_ADV_FLAG_GENERAL_DISC if limited_disc else _ADV_FLAG_GENERAL_DISC) | \
            (_ADV_FLAG_NO_BREDR if not br_edr else 0)
    payload += struct.pack("BB", 2, _ADV_TYPE_FLAGS)
    payload += struct.pack("B", flags)

    # Name
    if name:
        name_bytes = name.encode("utf-8")
        payload += struct.pack("BB", len(name_bytes) + 1, _ADV_TYPE_NAME)
        payload += name_bytes

    # Services (UUIDs)
    if services:
        for service in services:
            b = bytes(service)
            if len(b) == 2:
                payload += struct.pack("BB", len(b) + 1, _ADV_TYPE_UUID16_COMPLETE) + b
            elif len(b) == 4:
                payload += struct.pack("BB", len(b) + 1, _ADV_TYPE_UUID32_COMPLETE) + b
            elif len(b) == 16:
                payload += struct.pack("BB", len(b) + 1, _ADV_TYPE_UUID128_COMPLETE) + b

    return payload
