def serialize_str(stri):
    data = stri.encode("utf-8")
    packet = bytes([1]) + data
    return packet

def print_func(data):
    msg = data.decode("utf-8")
    print(msg)

