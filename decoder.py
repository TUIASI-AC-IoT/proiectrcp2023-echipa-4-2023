class decoder:

    def decode(packet):
        pass

    def decode_connect(packet):
        bytearray_login = bytearray(packet)
        username_len = bytearray_login[37]

        password_len = bytearray_login[37 + username_len + 2]

        username_start = 38
        username_end = username_start + username_len
        username = bytearray_login[username_start:username_end].decode("utf-8")

        password_start = username_end + 2
        password_end = password_start + password_len
        password = bytearray_login[password_start:password_end].decode("utf-8")

        return username, password

    def connac_packet(packet):
        if packet == b'\xc0\x00':
            return True
        return False
