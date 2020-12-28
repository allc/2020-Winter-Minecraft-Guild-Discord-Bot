def get_minecraft_server_address_port(address, port):
    if port is None:
        #TODO: Use of SRV record
        pass
    return (address, port)

def pack_varint(n):
    result = b''
    while True:
        tmp = n & 0b01111111
        n >>= 7
        if n != 0:
            tmp |= 0b10000000
        result += tmp.to_bytes(1, 'little')
        if n == 0:
            break
    return result

def unpack_varint(connection):
    result = 0
    for i in range(5):
        data = connection.recv(1)
        if len(data) == 0:
            break
        tmp = ord(data)
        result |= (tmp & 0x7F) << 7 * i
        if not tmp & 0x80:
            break
    return result
