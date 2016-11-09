import os
import serial.tools.list_ports


FIRMWARE_FILE = os.path.join(os.path.dirname(__file__), 'firmware/firmware-combined.bin')
KNOWN_SERIAL_DEVICES = ['/dev/ttyUSB0', 'dev/cu.SLAB_USBtoUART', '/dev/cu.wchusbserial', 'COM1']


def com_port_devices():
    return [port.device for port in serial.tools.list_ports.comports()]


def determine_default_serial_port():
    device = KNOWN_SERIAL_DEVICES[0]
    for device in com_port_devices():
        if device in KNOWN_SERIAL_DEVICES:
            return device
        for known in KNOWN_SERIAL_DEVICES:
            if device.startswith(known):
                return device
    return device
