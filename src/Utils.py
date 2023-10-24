def serialize_str(stri):
    data = stri.encode("utf-8")
    return data

def print_func(data, source):
    msg = data.decode("utf-8")
    print(msg)

