from . import helperFunctions

class CamelliaBase():

    def __init__(self, keyLenght, key, message):

        """ Function to initialize class object

        Parameters:
        keyLenght (int): Bit length of given key
        key (string): Key to be used for encryption
        message (string): Message to be encrypted
        
        """

        self.keyLenght = keyLenght
        self.key = key
        self.message = message
        self.s1, self.s2, self.s3, self.s4 = self.generateSBoxes()
        self.constants = [0xA09E667F3BCC908B,0xB67AE8584CAA73B2,0xC6EF372FE94F82BE,
                          0x54FF53A5F1D36F1C,0x10E527FADE682D1D,0xB05688C2B3E6C1FD]


    def rotateRightBy1(self, numberToBeRotated):

        """ Function that rotates binary value of the given input by one in circular fashion to right

        Parameters:
        numberToBeRotated (int): Value to be rotated

        Returns:
        int: The input value after rotating

        """

        numberToBeRotated = bin(numberToBeRotated)[2:]
        numberToBeRotated = helperFunctions.pad(numberToBeRotated, 8)
        numberToBeRotated = (numberToBeRotated[-1] + numberToBeRotated[:-1])
        numberToBeRotated = int(numberToBeRotated,2)
        return numberToBeRotated


    def evenThenUnvenList(listToBeSorted):

        """ Function that rearanges given list by first taking only characters on even indexes 
            (0, 2, 4, 6, ....) and then characters in uneven characters (1, 3, 5, 7, ...)

        Parameters:
        listToBeSorted (list): List of characters to be rearanged


        Returns:
        list: List of characters after rearanging

        """
        
        evenThenUnevenList = []
        for i in range (len(listToBeSorted)):
            if i % 2 == 0:
                evenThenUnevenList.append(listToBeSorted[i])
        for i in range (len(listToBeSorted)):
            if i % 2 != 0:
                evenThenUnevenList.append(listToBeSorted[i])
        return evenThenUnevenList


    def generateSBoxes(self):

        """ Function that creates S-boxes from first S-box (s1) and returns all four
            of them

        Parameters:

        Returns:
        s1 (list): First S-box (list of values)
        s2 (list): Second S-box (list of values)
        s3 (list): Third S-box (list of values)
        s4 (list): Fourth S-box (list of values)

        """

        s1=[112, 130, 44, 236, 179, 39, 192, 229, 228, 133, 87, 53, 234, 12, 174, 65,
            35, 239, 107, 147, 69, 25, 165, 33, 237, 14, 79, 78, 29, 101, 146, 189,
            134, 184, 175, 143, 124, 235, 31, 206, 62, 48, 220, 95, 94, 197, 11, 26,
            166, 225, 57, 202, 213, 71, 93, 61, 217, 1, 90, 214, 81, 86, 108, 77,
            139, 13, 154, 102, 251, 204, 176, 45, 116, 18, 43, 32, 240, 177, 132, 153,
            223, 76, 203, 194, 52, 126, 118, 5, 109, 183, 169, 49, 209, 23, 4, 215,
            20, 88, 58, 97, 222, 27, 17, 28, 50, 15, 156, 22, 83, 24, 242, 34,
            254, 68, 207, 178, 195, 181, 122, 145, 36, 8, 232, 168, 96, 252, 105, 80,
            170, 208, 160, 125, 161, 137, 98, 151, 84, 91, 30, 149, 224, 255, 100, 210,
            16, 196, 0, 72, 163, 247, 117, 219, 138, 3, 230, 218, 9, 63, 221, 148,
            135, 92, 131, 2, 205, 74, 144, 51, 115, 103, 246, 243, 157, 127, 191, 226,
            82, 155, 216, 38, 200, 55, 198, 59, 129, 150, 111, 75, 19, 190, 99, 46,
            233, 121, 167, 140, 159, 110, 188, 142, 41, 245, 249, 182, 47, 253, 180, 89,
            120, 152, 6, 106, 231, 70, 113, 186, 212, 37, 171, 66, 136, 162, 141, 250,
            114, 7, 185, 85, 248, 238, 172, 10, 54, 73, 42, 104, 60, 56, 241, 164,
            64, 40, 211, 123, 187, 201, 67, 193, 21, 227, 173, 244, 119, 199, 128, 158]
        
        s2 = []
        s3 = []
        s4 = []
        
        for i in range(len(s1)):
            if (s1[i]) != 255:
                s2.append((s1[i] << 1) % 255)
            else:
                s2.append(255)

            s3.append(self.rotateRightBy1(s1[i]))
            s4 = CamelliaBase.evenThenUnvenList(s1)
        
        return s1, s2, s3, s4


    def sFunction(self, BitInputToTransform):
        
        """ Function that splits 64-bit long intput into 8-bit long parts, converts them into int values
            and uses these values as indexes for substitution using "S-boxes"  

        Parameters:
        BitInputToTransform (string): String value for processing

        Returns:
        string : 64-bit long binary string of substituted values

        """

        BitInputToTransformArray = [BitInputToTransform[i:i+8] for i in range(0, len(BitInputToTransform), 8)]

        BitInputToTransformArray[0] = helperFunctions.pad(bin(self.s1.index(int(BitInputToTransformArray[0],2)))[2:],8)
        BitInputToTransformArray[1] = helperFunctions.pad(bin(self.s2.index(int(BitInputToTransformArray[1],2)))[2:],8)
        BitInputToTransformArray[2] = helperFunctions.pad(bin(self.s3.index(int(BitInputToTransformArray[2],2)))[2:],8)
        BitInputToTransformArray[3] = helperFunctions.pad(bin(self.s4.index(int(BitInputToTransformArray[3],2)))[2:],8)
        BitInputToTransformArray[4] = helperFunctions.pad(bin(self.s2.index(int(BitInputToTransformArray[4],2)))[2:],8)
        BitInputToTransformArray[5] = helperFunctions.pad(bin(self.s3.index(int(BitInputToTransformArray[5],2)))[2:],8)
        BitInputToTransformArray[6] = helperFunctions.pad(bin(self.s4.index(int(BitInputToTransformArray[6],2)))[2:],8)
        BitInputToTransformArray[7] = helperFunctions.pad(bin(self.s1.index(int(BitInputToTransformArray[7],2)))[2:],8)

        return ''.join(BitInputToTransformArray)


    def pFunction(self, BitInputToTransform):
                
        """ Function that splits 64-bit long intput into 8-bit long parts, converts them into int values
            and XORs them as defined in specification of the cipher

        Parameters:
        BitInputToTransform (string): String value for processing

        Returns:
        string : 64-bit long binary string of XORed values

        """

        BitInputToTransformArray = [int(BitInputToTransform[i:i+8],2) for i in range(0, len(BitInputToTransform), 8)]
        BitInputToTransformArrayCopy = []

        BitInputToTransformArrayCopy.append(BitInputToTransformArray[0] ^ BitInputToTransformArray[2] ^ BitInputToTransformArray[3] ^ BitInputToTransformArray[5] ^ BitInputToTransformArray[6] ^ BitInputToTransformArray[7])
        BitInputToTransformArrayCopy.append(BitInputToTransformArray[0] ^ BitInputToTransformArray[1] ^ BitInputToTransformArray[3] ^ BitInputToTransformArray[4] ^ BitInputToTransformArray[6] ^ BitInputToTransformArray[7])
        BitInputToTransformArrayCopy.append(BitInputToTransformArray[0] ^ BitInputToTransformArray[1] ^ BitInputToTransformArray[2] ^ BitInputToTransformArray[4] ^ BitInputToTransformArray[5] ^ BitInputToTransformArray[7])
        BitInputToTransformArrayCopy.append(BitInputToTransformArray[1] ^ BitInputToTransformArray[2] ^ BitInputToTransformArray[3] ^ BitInputToTransformArray[4] ^ BitInputToTransformArray[5] ^ BitInputToTransformArray[6])
        BitInputToTransformArrayCopy.append(BitInputToTransformArray[0] ^ BitInputToTransformArray[1] ^ BitInputToTransformArray[5] ^ BitInputToTransformArray[6] ^ BitInputToTransformArray[7])
        BitInputToTransformArrayCopy.append(BitInputToTransformArray[1] ^ BitInputToTransformArray[2] ^ BitInputToTransformArray[4] ^ BitInputToTransformArray[6] ^ BitInputToTransformArray[7])
        BitInputToTransformArrayCopy.append(BitInputToTransformArray[2] ^ BitInputToTransformArray[3] ^ BitInputToTransformArray[4] ^ BitInputToTransformArray[5] ^ BitInputToTransformArray[7])
        BitInputToTransformArrayCopy.append(BitInputToTransformArray[0] ^ BitInputToTransformArray[3] ^ BitInputToTransformArray[4] ^ BitInputToTransformArray[5] ^ BitInputToTransformArray[6])

        for i in range(len(BitInputToTransformArrayCopy)):
            BitInputToTransformArrayCopy[i] = bin(BitInputToTransformArrayCopy[i])[2:]
            BitInputToTransformArrayCopy[i] = helperFunctions.pad(BitInputToTransformArrayCopy[i],8)   
        return ''.join(BitInputToTransformArrayCopy)


    def fFunction(self, BitInputToTransform, Key):
                        
        """ Function that converts given input into int, XORs it with given key. Result of these operations
            is then used as input to "S-function" and that result is then used as input into "P-function" and
            result of "P-function" is then returned.


        Parameters:
        BitInputToTransform (string) : String value for processing
        Key (int) : Given key

        Returns:
        output (string) : 64-bit long binary string

        """

        BitInputToTransform = int(BitInputToTransform,2)
        inputXORKey = BitInputToTransform ^ Key
        inputXORKey = helperFunctions.pad(bin(inputXORKey)[2:],64)
        output = self.pFunction(self.sFunction(inputXORKey))
        return output


    def flFunction(self, BitInputToTransform, kl):
                                
        """ Function that that takes 64-bit long input and given "kl" subkey and splits them into 32-bit long 
            (left and right) parts. 

            Right 32-bits of output are created by AND-ing left 32 bits of input and left 32 bits of "kl" subkey. 
            Result of this operation is then rotated in circular fashion by 1 bit to the left 
            and XOR-ed with right 32 bits of input.

            Left 32-bits od output are created by OR-ing right 32 bits of output created in previous steps
            and right 32 bits of "kl" subkey. Result of this operation is then XOR-ed with left 32 bits of input.
            

        Parameters:
        BitInputToTransform (string) : String value for processing
        kl (int) : Given "kl" subkey

        Returns:
        string : 64-bit long binary string created as concatenation of left and right 32 bit long
                 parts of output

        """

        BitInputToTransformL = BitInputToTransform[:32]
        BitInputToTransformR = BitInputToTransform[32:]
        kll = kl[:32]
        klr = kl[32:]
        outputR = int(BitInputToTransformL,2) & int(kll,2)
        outputR = helperFunctions.rotateLeft(bin(outputR)[2:],32,1)
        outputR = helperFunctions.pad(bin(outputR ^ int(BitInputToTransformR,2))[2:],32)
        outputL = int(outputR,2) | int(klr,2)
        outputL = helperFunctions.pad(bin(outputL ^ int(BitInputToTransformL,2))[2:],32)
        return ''.join(outputL + outputR)


    def flminusFunction(self, BitInputToTransform, kl):
                                        
        """ Function that that takes 64-bit long input and given "kl" subkey and splits them into 32-bit long 
            (left and right) parts. 

            Left 32-bits of output are created by OR-ing right 32 bits of input and right 32 bits of "kl" subkey. 
            Result of this operation is then XOR-ed with left 32 bits of input.

            Right 32-bits of output are created by AND-ing left 32 bits of input and left 32 bits of "kl" subkey. 
            Result of this operation is then rotated in circular fashion by 1 bit to the left 
            and XOR-ed with right 32 bits of input.
            

        Parameters:
        BitInputToTransform (string) : String value for processing
        kl (int) : Given "kl" subkey

        Returns:
        string : 64-bit long binary string created as concatenation of left and right 32 bit long
                 parts of output

        """

        BitInputToTransformL = BitInputToTransform[:32]
        BitInputToTransformR = BitInputToTransform[32:]
        kll = kl[:32]
        klr = kl[32:]
        outputL = int(BitInputToTransformR,2) | int(klr,2)
        outputL = helperFunctions.pad(bin(outputL ^ int(BitInputToTransformL,2))[2:],32)
        outputR = int(outputL,2) & int(kll,2)
        outputR = helperFunctions.rotateLeft(bin(outputR)[2:],32,1)
        outputR = helperFunctions.pad(bin(outputR ^ int(BitInputToTransformR,2))[2:],32)
        return ''.join(outputL + outputR)