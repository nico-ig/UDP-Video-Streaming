def fragment_binary(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    fragment_size = 1024  # Change this to adjust the size of each fragment
    binary_fragments = [binary_data[i:i+fragment_size] for i in range(0, len(binary_data), fragment_size)]
    return binary_fragments

# Example usage
binary_fragments = fragment_binary('path/to/file')
