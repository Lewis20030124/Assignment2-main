import sys
from bitarray import bitarray

def decode(ba: bitarray):
    # decode elias for the length of the orgianl string
    (length, next_section_start) = decode_elias(ba, 0)
    print("Length of the original string is: ", length, "next_section_start: ", next_section_start)
    total_length = length

    # decode elias for total number of unique characters
    (total_chars, next_section_start) = decode_elias(ba, next_section_start)
    print("Total number of unique characters is: ", total_chars, "next_section_start: ", next_section_start)

    huffman_result = {}
    # decode the rest of the header
    for i in range(total_chars):
        # Decode the ASCII value of the character
        #the next 7 bits represent the ASCII value of the character
        ascii_value = int(ba[next_section_start:next_section_start+7].to01(), 2)
        next_section_start = next_section_start + 7
        #ascii to character
        char = chr(ascii_value)

        #decode the elias code for the length of the huffman code
        (length, next_section_start) = decode_elias(ba, next_section_start)
        #get the huffman code
        decoded_huffman_code = ba[next_section_start:next_section_start+length].to01()
        next_section_start = next_section_start + length
        #store the huffman code
        huffman_result[decoded_huffman_code] = char

    print("Huffman result: ", huffman_result)

    # find the max length of the huffman code
    max_length = 0
    for key in huffman_result.keys():
        if len(key) > max_length:
            max_length = len(key)
    # decode data part 
    bwt_res = ""
    # check for if any part matches the the huffman result 
    while len(bwt_res) < total_length:
        for i in range(1, max_length+1):
            if ba[next_section_start:next_section_start+i].to01() in huffman_result.keys():
                new_next_section_start = next_section_start+i

                #find the length of the elias code for the number of appearances of the character
                (appearances, new_next_section_start) = decode_elias(ba, new_next_section_start)
                #store the character in the bwt_res
                bwt_res += huffman_result[ba[next_section_start:next_section_start+i].to01()]*appearances
                next_section_start = new_next_section_start
                break

    # decode the bwt_res
    original_string = reverse_bwt(bwt_res)
    print("Original string: ", original_string)
    

def reverse_bwt(bwt_res: str):
    """
    This function implements the reverse Burrows-Wheeler Transform
    Parameters:
    bwt_res: str, the transformed string
    Returns:
    str, the original string
    """
    orig_index = bwt_res.index('$')
    
    # Initialize the table where rows will be stored
    table = [""] * len(bwt_res)
    
    # Repeatedly insert the BWT as a new column of chars before current rows
    for i in range(len(bwt_res)):
        # Prepend bwt characters to each row string
        table = [bwt_res[j] + table[j] for j in range(len(bwt_res))]
        # Sort the table row-wise (lexicographically)
        table.sort()

    # The original string ends with the original end-of-file character, so return the row that has it
    return table[orig_index]


        


    
def decode_elias(ba: bitarray, start_index):
    """
    The logic is to decode the fist bit, covert it to '1' if its '0', then use the "length" converted from '1' to 
    get the next section of the Elias code. Which is "length" +1, start from the "start index".
    The end of the Elias code is when the section starts from '1'
    param: ba: bitarray, contains the encoded Elias code
    """
    if ba[0] == '1':
        # If the first bit is 1, the Elias code is 1, means the length is 1
        return 1

    length = 0
    final = False # flag to indicate the end of the Elias code, when a section starts from 1 
    # Decode the Elias code
    while not final:
        #change the first bit of the ba to 1
        if ba[start_index] == False:
            ba[start_index] = True
        else:
            final = True

        # Convert the bitarray from start to length to an integer
        new_length = int(ba[start_index:start_index+length+1].to01(), 2)
        
        #update the start index
        start_index = start_index + length +1

        #update the length
        length = new_length


    return (length, start_index)

def main(binary_file):
    # Read the binary file
    ba = bitarray()

    # Open the binary file for reading in binary mode ('rb').
    with open(binary_file, 'rb') as file:
        # Use the fromfile() method of bitarray to read the entire content of
        # the file into the bitarray. This method reads bytes from the file
        # and converts them into bits, appending to the bitarray 'ba'.
        ba.fromfile(file)

    result = decode(ba)

    # Save the recovered string to 'q2_decoder_output.txt'
    with open('q2_decoder_output.txt', 'w') as file:
        #file.write(original_string)
        pass

if __name__ == "__main__":
    """     
    if len(sys.argv) != 2:
        print("Usage: python q2_decoder.py <binary file generated by your encoder>")
        sys.exit(1)
    main(sys.argv[1]) 
    """
    main("/Users/lewis/Monash/FIT3155 Advanced Algo/Assignment2-main/Assignment2-main/q2_encoder_output.bin")
