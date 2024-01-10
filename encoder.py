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
        0x8E,
        0x00,
    ])
    return disconnect_packet


def generate_suback(qos):
    suback_packet = bytearray([
        0x0B,
        0x26,
        0x05,
        qos,
        0x02
    ])
    return suback_packet


def generate_puback():
    puback_packet = bytearray([
        0x40,
        0x04,
        0x64,
        0x4A,
        0x10,
        0x00
    ])
    return puback_packet


def generate_pingresp():
    pingresp_pascket = bytearray([
        0xD0,
        0x00
    ])
    return pingresp_pascket

def generate_suback_packet(packet_id, qos_level):
    suback_packet = bytearray([0x90,
                               0x03,
                               (packet_id >> 8) & 0xFF,
                               packet_id & 0xFF,
                               qos_level])
    return suback_packet


def generate_pubrec_packet(packet_id):
    return bytes([0x50,
                  0x02,
                  (packet_id >> 8) & 0xFF,
                  packet_id & 0xFF])

def generate_pubcomp_packet(packet_id):
    return bytes([0x70,
                  0x02, (packet_id >> 8) & 0xFF,
                  packet_id & 0xFF])

