import sys
from bitarray import bitarray

def encoder(s: str):
    """
    This function implements the encoder for the given input string
    Parameters:
    string: str, the input string
    Returns:
    bitarray: the encoded bitarray
    """
    bitArray = bitarray()
    # Apply the Burrows-Wheeler Transform
    bwt_res = bwt(s)
    # Elias Code 
    elias_res = EliasCode(len(bwt_res))
    bitArray.extend(elias_res)

    # Huffman Encoding
    huffman_res = huffman_encode(bwt_res)
    # Get total number of unqiue characters
    total_chars = len(huffman_res)

    # Elias Code of total number of unique characters 
    elias_res = EliasCode(total_chars)
    bitArray.extend(elias_res)

    # Get bit value of each character + elias code length + huffmancode of each character
    for key in huffman_res:
        #get bit value of each character
        char = key
        ascii_value = ord(char)  # Get ASCII value
        binary_value = bin(ascii_value)[2:]  # Convert to binary and remove '0b' prefix
        padded_binary_value = binary_value.zfill(7)  # Pad with zeros to make it 8 bits
        bitArray.extend(padded_binary_value)
        #get elias code length of each character's huffman code
        elias_res = EliasCode(len(huffman_res[key]))
        bitArray.extend(elias_res)
        #get huffman code of each character
        bitArray.extend(huffman_res[key])

    # Run Length Encoding
    rle_res = rle(bwt_res)

    # Get huffman code of each character in rle_res + elias code the number of appearances of each character
    for key in rle_res:
        #get huffman code of each character
        char = key[0]
        huffman_code = huffman_res[char]
        bitArray.extend(huffman_code)
        #get elias code the number of appearances of each character
        elias_res = EliasCode(key[1])
        bitArray.extend(elias_res)
    
    #padd the bitarray to make it a multiple of 8
    while len(bitArray) % 8 != 0:
        bitArray.extend('0')
    return bitArray


def bwt(s: str):
    """
    This function implements the Burrows-Wheeler Transform
    Parameters:
    string: str, the input string
    Returns:
    tuple: (str, int), the transformed string and the index of the original string in the sorted list of cyclic rotations
    """
    if s[-1] != '$':
        s += '$'
    # Generate all cyclic rotations of the string
    n = len(s)
    table = [s[i:] + s[:i] for i in range(n)]
    # Sort the rotations
    table_sorted = sorted(table)
    # Extract the last column from the sorted rotations
    last_column = ''.join(row[-1] for row in table_sorted)
    
    return last_column

def rle(s: str) -> str:
    """
    This function implements the Run-Length Encoding
    Parameters:
    string: str, the input string
    Returns:
    str: the encoded string
    """
    # Initialize the encoded string
    encoded = []
    # Initialize the count of the current character
    count = 1
    # Iterate through the string
    for i in range(1, len(s)):
        # If the current character is the same as the previous character
        if s[i] == s[i-1]:
            # Increment the count
            count += 1
        else:
            # Append the character and the count to the encoded string
            encoded.append((s[i-1],count))
            # Reset the count
            count = 1
    # Append the last character and the count to the encoded string
    encoded.append((s[-1],count))
    return encoded

def EliasCode(num: int):
    """
    This function implements the Elias Omega Encoding
    Parameters:
    num: int, the input number
    Returns:
    binary: the encoded binary string
    """
    result = ""
    bitarray = bin(num)[2:]
    result += bitarray
    while len(bitarray) > 1:
        bitarray = EliasCodeEncode(len(bitarray)-1)
        #change leading 1 to 0 
        if bitarray[0] == '1':
            bitarray = '0' + bitarray[1:]
        result = bitarray + result
    return result

def EliasCodeEncode(num: int):
    bitarray = bin(num)[2:]
    return bitarray


class Node:
    """
    This class represents a node in the Huffman tree
    """
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def huffman_encode(text):
    frequencies = count_frequencies(text)
    nodes = build_nodes(frequencies)
    root = merge_nodes(nodes)
    codebook = assign_codes(root)

    print("codebook", codebook)

    #sort codebook by key in aplhabetical order
    codebook = dict(sorted(codebook.items()))
    #make sure $ goes last 
    codebook['$'] = codebook.pop('$')
    print("codebook", codebook)
    return codebook

def count_frequencies(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    print(frequency)
    return frequency

def build_nodes(frequency):
    nodes = []
    for char in frequency:
        nodes.append(Node(char, frequency[char]))
    return sorted(nodes, key=lambda node: node.freq)

def merge_nodes(nodes):
    while len(nodes) > 1:
        # Sort nodes based on frequency each time we modify the list
        nodes = sorted(nodes, key=lambda node: node.freq)

        left = nodes.pop(0)
        right = nodes.pop(0)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        nodes.append(merged)

    return nodes[0]

def assign_codes(node, prefix="", codebook={}):
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        assign_codes(node.left, prefix + '0', codebook)
        assign_codes(node.right, prefix + '1', codebook)
    return codebook

def main(file_name):
    """Read file, encode content, and write output."""
    with open(file_name, 'r') as file:
        input_string = file.read().strip()
    
    encoded_bitarray = encoder(input_string)
    
    with open("q2_encoder_output.bin", "wb") as output_file:
        output_file.write(encoded_bitarray.tobytes())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python q2_encoder.py <stringFileName>")
    else:
        main(sys.argv[1])