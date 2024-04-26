def bwt(s: str) -> (str, int):
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
    print(table)
    
    # Sort the rotations
    table_sorted = sorted(table)
    
    # Extract the last column from the sorted rotations
    last_column = ''.join(row[-1] for row in table_sorted)
    
    # Optional: To support decoding, find the index of the original string in the sorted list
    original_index = table_sorted.index(s)
    
    return (last_column, original_index)

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
    encoded.append((s[i-1],count))
    
    return encoded

if __name__ == "__main__":
    res = bwt("banana")
    print(res)
    print(rle(res[0]))
    