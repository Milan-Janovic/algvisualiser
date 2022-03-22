import random
from . import helperFunctions

class ChaCha20():

    def __init__(self, key, message):

        """ Function to initialize class object

        Parameters:
        key (string): Key to be used for encryption
        message (string): Message to be encrypted
        
        """

        self.key = key
        self.message = message
        self.constant = list("expand 32-byte k")
        self.max32bitInteger = (pow(2,32) - 1)


    def processConstant(self):

        """ Function to convert each character in costant to its binary representation based
            on its ASCII value

        Parameters:

        Returns:
        list: List of binary representations of every character in constant
        
        """

        for i in range(len(self.constant)):
            self.constant[i] = helperFunctions.pad(bin(ord(self.constant[i]))[2:],8)

        return self.constant


    def generateConstantParts(self, constant):
        
        """ Function that takes every four binary values from constant, concatenates them
            and converts created binary value to int

        Parameters:
        constant (list): List of binary representations of every character in constant  

        Returns:
        iconstant (list): List of 4 integer values each created from 4 of 16 binary values in constant
        
        """
        
        iconstant = [constant[i:i+4] for i in range(0, len(constant), 4)]
        iconstant = [''.join(iconstant[i]) for i in range(len(iconstant))]
        iconstant = [int(iconstant[i],2) for i in range(len(iconstant))]
        return iconstant


    def splitKey(self, key):

        """ Function that splits 256 bits long key into eight 32 bit long values
            and converts them to int 

        Parameters:
        key (string): String consisting of 256 bits of key

        Returns:
        ikey (list): List of 8 integer values each created from 32 bits of 256 bits long key
        
        """

        ikey = [key[i:i+32] for i in range(0, len(key), 32)]
        ikey = [''.join(ikey[i]) for i in range(len(ikey))]
        ikey = [int(ikey[i],2) for i in range(len(ikey))]
        return ikey


    def getRandomNumber96Bits(self):
                
        """ Function that creates 12 random values and pads them to be 8 bits long,
            then creates 96 bit long value by concatenating them
            
        Returns:
        n (string): 96 bit long value (created as stated before)
        
        """

        n = list(str(random.randint(100000000000,999999999999)))
        for i in range(len(n)):
            n[i] = helperFunctions.pad(bin(int(n[i],10))[2:],8)
        n = ''.join(n)
        return n


    def splitNonce(self, nonce):
                       
        """ Function that splits 96 bits long nonce into three 32 bit long values
            and converts them to int 

        Parameters:
        nonce (string): String consisting of 96 bits of nonce

        Returns:
        inonce (list): List of 3 integer values each created from 32 bits of 96 bits long nonce
        
        """

        inonce = [nonce[i:i+32] for i in range(0, len(nonce), 32)]
        inonce = [int(inonce[i],2) for i in range(len(inonce))]
        return inonce


    def generateMatrix(self, constant, key, blockNumber, nonce):
                     
        """ Function that generates matrix as specificed in ChaCha documentation

        Parameters:
        iconstant (list): List of four 32 bit values of constants (in integer representation)
        ikey (list): List of eight 32 bit values of key (in integer representation)
        blockNumber (int): Number of block for encryption (in our case is always 1)
        inonce (list): List of three 32 bit values of nonce (in integer representation)

        Returns:
        matirx (list): 4x4 matrix as specificed in ChaCha documentation
        
        """

        iblockNumber = blockNumber
        

        matrix = [  [constant[0],  constant[1],  constant[2],  constant[3]],
                    [key[0],       key[1],       key[2],       key[3]     ],
                    [key[4],       key[5],       key[6],       key[7]     ],
                    [blockNumber,  nonce[0],     nonce[1],     nonce[2]   ]  ]
        return matrix


    def quaterRoundFunction(self, a,b,c,d):
                             
        """ Function used on matrix in rounds in order to change certain elements from it
            (by using algebraic and bit-wise operations on the element) depending on round

        Parameters:
        a (int): One of elements from matrix
        b (int): One of elements from matrix
        c (int): One of elements from matrix
        d (int): One of elements from matrix

        Returns:
        a (int): One of elements from matrix after change
        b (int): One of elements from matrix after change
        c (int): One of elements from matrix after change
        d (int): One of elements from matrix after change
        
        """

        a = (a + b) % self.max32bitInteger
        d = d ^ a
        d = helperFunctions.rotateLeft(bin(d)[2:], 32, 16)
        
        c = (c + d)  % self.max32bitInteger
        b = b ^ c
        b = helperFunctions.rotateLeft(bin(b)[2:], 32, 12)
        
        a = (a + b)  % self.max32bitInteger
        d = d ^ a
        d = helperFunctions.rotateLeft(bin(d)[2:], 32, 8)
        
        c = (c + d)  % self.max32bitInteger
        b = b ^ c
        b = helperFunctions.rotateLeft(bin(b)[2:], 32, 7)
        return a, b, c, d


    def columnRoundFunction(self, matrix):

        """ Function that calls "quaterRoundFunction" on matrix in column fashion

        Parameters:
        matrix (list): 4x4 matrix created in "generateMatrix" function (values may have changed since creation)

        Returns:
        matrix (list): 4x4 matrix created in "generateMatrix" function after each column
                       was changed by calling "quaterRoundFunction" on it
        
        """

        matrix[0][0], matrix[1][0], matrix[2][0], matrix[3][0] = self.quaterRoundFunction(matrix[0][0], matrix[1][0], matrix[2][0], matrix[3][0])
        matrix[0][1], matrix[1][1], matrix[2][1], matrix[3][1] = self.quaterRoundFunction(matrix[0][1], matrix[1][1], matrix[2][1], matrix[3][1])
        matrix[0][2], matrix[1][2], matrix[2][2], matrix[3][2] = self.quaterRoundFunction(matrix[0][2], matrix[1][2], matrix[2][2], matrix[3][2])
        matrix[0][3], matrix[1][3], matrix[2][3], matrix[3][3] = self.quaterRoundFunction(matrix[0][3], matrix[1][3], matrix[2][3], matrix[3][3])
        return matrix


    def diagonalRoundFunction(self, matrix):

        """ Function that calls "quaterRoundFunction" on matrix in diagonal fashion

        Parameters:
        matrix (list): 4x4 matrix created in "generateMatrix" function (values may have changed since creation)

        Returns:
        matrix (list): 4x4 matrix created in "generateMatrix" function after each diagonal
                       was changed by calling "quaterRoundFunction" on it
        
        """

        matrix[0][0], matrix[1][1], matrix[2][2], matrix[3][3] = self.quaterRoundFunction(matrix[0][0], matrix[1][1], matrix[2][2], matrix[3][3])
        matrix[0][1], matrix[1][2], matrix[2][3], matrix[3][0] = self.quaterRoundFunction(matrix[0][1], matrix[1][2], matrix[2][3], matrix[3][0])
        matrix[0][2], matrix[1][3], matrix[2][0], matrix[3][1] = self.quaterRoundFunction(matrix[0][2], matrix[1][3], matrix[2][0], matrix[3][1])
        matrix[0][3], matrix[1][0], matrix[2][1], matrix[3][2] = self.quaterRoundFunction(matrix[0][3], matrix[1][0], matrix[2][1], matrix[3][2])
        return matrix


    def encryptChaCha20(self, PT, constant, key, nonce):

        """ Function that encrypts given input with given key using ChaCha algorithm

        Parameters:
        PT (string): Plain text converted into binary string
        constant (list): List of four integer values created from constant in "generateConstantParts" function
        key (list): List of eight integer values created from key in "splitKey" function
        nonce (list): List of three integer values created from nonce in "splitNonce" function

        Returns:
        CT (list): Cipher text splited into list form of 32 bit long parts
        matrixFlat (list): Matrix used to encrypt PT into CT, flattened into one dimensional array
        PT (list): PT splitted into 32 bit long parts and converted into int

        """

        matrix = self.generateMatrix(constant, key, 1, nonce)
        matrixInit = matrix
        
        for i in range(10):
            matrix = self.columnRoundFunction(matrix)
            matrix = self.diagonalRoundFunction(matrix)  
        
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] = (matrix[i][j] + matrixInit[i][j])  % self.max32bitInteger

            
        PT = [int(PT[i:i+32],2) for i in range(0, len(PT), 32)]
        
        matrixFlat = list()
        for item in matrix:
            matrixFlat += item
                   
        CT = list()
        
        for i in range(len(PT)):
            CT.append(helperFunctions.pad(bin(PT[i] ^ matrixFlat[i])[2:],32))

        return CT, matrixFlat, PT


    def decryptChaCha20(self, CT, constant, key, nonce):

        """ Function that dencrypts given input with given key using ChaCha algorithm

        Parameters:
        CT (string): Cipher text converted into binary string
        constant (list): List of four integer values created from constant in "generateConstantParts" function
        key (list): List of eight integer values created from key in "splitKey" function
        nonce (list): List of three integer values created from nonce in "splitNonce" function

        Returns:
        PT (list): PT after decryption splitted into 32 bit long parts
        CT (list): Cipher text splited into list form of 32 bit long parts and converted into int

        """

        matrix = self.generateMatrix(constant, key, 1, nonce)
        matrixInit = matrix
        
        for i in range(10):
            matrix = self.columnRoundFunction(matrix)
            matrix = self.diagonalRoundFunction(matrix)
        
            
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] = (matrix[i][j] + matrixInit[i][j])  % self.max32bitInteger
                
        CT = ''.join(CT)
        CT = [int(CT[i:i+32],2) for i in range(0, len(CT), 32)]
        
        matrixFlat = list()
        for item in matrix:
            matrixFlat += item
        
        PT = list()
       
        for i in range(len(CT)):
            PT.append(helperFunctions.pad(bin(CT[i] ^ matrixFlat[i])[2:],32))
            
        return PT, CT