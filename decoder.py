class decoder:

    def decode(packet):
        pass

    def decode_connect(packet):
        bytearray_login = bytearray(packet)

        keep_alive_bytes = packet[10:12]
        print(keep_alive_bytes)
        keep_alive_seconds = int.from_bytes(keep_alive_bytes, byteorder='big')
        username_len = bytearray_login[37]

        password_len = bytearray_login[37 + username_len + 2]

        username_start = 38
        username_end = username_start + username_len
        username = bytearray_login[username_start:username_end].decode("utf-8")

        password_start = username_end + 2
        password_end = password_start + password_len
        password = bytearray_login[password_start:password_end].decode("utf-8")
        return username, password,keep_alive_seconds

    def decode_publish_packet(publish_packet):
        topic = publish_packet[15:18].decode('utf-8')
        qos = int.from_bytes(publish_packet[20:21], byteorder='big')
        return topic, qos




