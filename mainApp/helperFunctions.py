def pad(inputToPad, padTo):

    """ Function that pads given bit string to desired length by adding 0
        to beggining of the string

    Parameters:
    inputToPad (str): Bit value to be padded
    padTO (int): Length to pad the input to (in bit length) 

    Returns:
    str: The input after padding

    """

    inputToPad = str(inputToPad)
    while(len(inputToPad) != padTo):
        inputToPad = '0' + inputToPad

    return inputToPad


def processInput(Key, Message):

    """ Function that changes input from string to binary represantation of each character
        based on their ASCII value

    Parameters:
    Key (str): Key to be processed
    Message (str): Message to be processed

    Returns:
    message_ascii (str): Message after processing
    key_ascii (str): Key after processing

    """

    key = list(Key)
    key_ascii = ''.join([pad(bin(ord(char))[2:],8) for char in key])
    message = list(Message)
    message_ascii = ''.join([pad(bin(ord(char))[2:],8) for char in message])
    return message_ascii, key_ascii


def rotateLeft(numberToBeRotated, padTo, rotateBy):

    """ Function that rotates binary value of the given input by given number of steps 
        in circular fashion to left

    Parameters:
    numberToBeRotated (str): Value to be rotated (in binary representation)
    padTo (int): Binary length that the input is supposed to be padded
    rotateBy (int): Defines number of steps that the input is supposed to be rotated


    Returns:
    int: The input value after rotating

    """

    numberToBeRotated = pad(numberToBeRotated, padTo)
    
    for i in range(rotateBy):
        numberToBeRotated = numberToBeRotated[1:] + numberToBeRotated[0]   
    numberToBeRotated = int(numberToBeRotated,2)
    return numberToBeRotated


def getCharacters(binaryValueToConvert):

    """ Function that changes int input back to its character representation

    Parameters:
    binaryValueToConvert (str): Value (in binary representation) to be processed

    Returns:
    str: The input value after processing --> in form of sentence

    """

    integerToConvert = [binaryValueToConvert[i:i+8] for i in range(0, len(binaryValueToConvert), 8)]
    integerToConvertASCII = [chr(int(integer,2)) for integer in integerToConvert]
    return ''.join(integerToConvertASCII)


def getCharactersKuznyechik(binaryValueToConvert):

    """ Function that changes int input back to its character representation for Kuznyechik algorithm

    Parameters:
    binaryValueToConvert (str): Value (in binary representation) to be processed

    Returns:
    str: The input value after processing --> in form of sentence

    """
    
    binaryValueToConvert = binaryValueToConvert[::-1]
    integerToConvert = [binaryValueToConvert[i:i+8] for i in range(0, len(binaryValueToConvert), 8)]
    for i in range(len(integerToConvert)):
        integerToConvert[i] = integerToConvert[i][::-1]
    integerToConvertASCII = [chr(int(integer,2)) for integer in integerToConvert]
    return ''.join(integerToConvertASCII)[::-1]