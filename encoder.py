import struct


def generate_connack_packet():
    connack_packet = bytearray([
        0x20,
        0x02,
        0x01,
        0x00
    ])
    return connack_packet


def generate_disconnect_packet():
    disconnect_packet = bytearray([
        0xE0,
        0x02,
        0x00,
        0x00
    ])
    return disconnect_packet
