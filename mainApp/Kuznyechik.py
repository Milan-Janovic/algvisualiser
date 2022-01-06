from . import helperFunctions
from . import kuznyechikLinearFunction

class Kuznyechik():

    def __init__(self, key, message):

        """ Function to initialize class object

        Parameters:
        key (string): Key to be used for encryption
        message (string): Message to be encrypted
        
        """

        self.key = key
        self.message = message


    def X(self, k, a):
        
        """ Function that XORs given input integers and returns the result

        Parameters:
        k (int): Integer to be XORed
        a (int): Integer to be XORed
        
        
        Returns:
        int : Result of "k" XOR "a"

        """

        return k ^ a


    def S(self, x): 
                
        """ Function that converts given int input "x" into list of 16 integer values, each
            representing 8 bits of the input and uses these values as indexes for substitution
            using "Pi" vector.

        Parameters:
        x (int): Integer value to be processed
        
        
        Returns:
        out (int) : Integer value created from concatenating 8-bit long binary values after
                    substitution

        """

        x = helperFunctions.pad(bin(x)[2:], 128)

        input_list = [int(x[i:i+8], 2) for i in range(0, len(x), 8)]

        for i in range(len(input_list)):
            input_list[i] = helperFunctions.pad(bin(self.Pi[input_list[i]])[2:], 8)

        out = int(''.join(input_list), 2)

        return out


    def S_inverse(self, x):

        """ Reverse function of function "S" defined above. Uses same steps as "S" function, but uses "Pi_neg"
            instead of "Pi" vector, which negates substitution done in "S" function

        Parameters:
        x (int): Integer value to be processed
        
        
        Returns:
        out (int) : Integer value created from concatenating 8-bit long binary values after
                    'reverse' substitution

        """

        x = helperFunctions.pad(bin(x)[2:], 128)

        input_list = [int(x[i:i + 8], 2) for i in range(0, len(x), 8)]

        for i in range(len(input_list)):
            input_list[i] = helperFunctions.pad(bin(self.Pi_neg[input_list[i]])[2:], 8)

        out = int(''.join(input_list), 2)

        return out


    def R(self, x):
        
        """ Function that takes integer x as input and applies kuznyechik_linear_function on it,
            moves the result to the left by 120 bits and XORs it with iniatial value of 'x' rotated
            by 8 bits to right.

        Parameters:
        x (int): Integer value to be processed
        
        
        Returns:
        a15 (int) : Integer value created from value 'x'

        """

        a15 = kuznyechikLinearFunction.kuznyechik_linear_function(x)
        a15 <<= 8 * 15
        a15 ^= (x >> 8)
        return a15


    def R_inverse(self, x):
       
        """ Inverse function of function 'R' above

        Parameters:
        x (int): Integer value to be processed
        
        
        Returns:
        (int) : Integer value created from value 'x'

        """

        a = x >> 15 * 8
        x = (x << 8)
        cut = len(bin(x)) - 128
        x = int(bin(x)[cut:], 2)
        b = kuznyechikLinearFunction.kuznyechik_linear_function(x ^ a)
        return x ^ b


    def L(self, x):
               
        """ Function that takes integer value as input and applies function 'R' on it 16 times

        Parameters:
        x (int): Integer value to be processed
        
        
        Returns:
        x (int) : Integer value created from initial 'x' value after 16 rounds of 'R' function
                  were applied in it

        """

        for i in range(16):
            x = self.R(x)
        return x


    def L_inverse(self, x):
                       
        """ Inverse function of function 'L' above

        Parameters:
        x (int): Integer value to be processed
        
        
        Returns:
        x (int) : Integer value created from initial 'x' value after 16 rounds of 'L_inverse' function
                  were applied in it

        """

        for i in range(16):
            x = self.R_inverse(x)
        return x


    def generateSubKeys(self, key256):
        
        """ Function that creates subkeys needed for encryption from initial value of given key

        Parameters:
        key256 (int): Given key
        
        
        Returns:
        keys (list) : List of integer values of subkeys to be used for encryption
        c_list (list) : List of integer values of constants used to create subkeys,
                        needed for visualisation purposes

        """

        keys = list()
        key256 = bin(key256)[2:]
        
        keyL = int(key256[:128], 2)
        keyR = int(key256[128:], 2)
        keys.append(keyL)
        keys.append(keyR)

        c_list = list()
        for i in range(1, 33):
            c = self.L(i)
            c_list.append(c)

        for i in range(4):
            for j in range(8):
                (keyL, keyR) = (self.L(self.S(self.X(keyL, c_list[8 * i + j]))) ^ keyR, keyL)

            keys.append(keyL)
            keys.append(keyR)
        return keys, c_list


    def encryptKuznyechik(self, PT, key):

        """ Function that encrypts given input with given key using Kuznyechik algorithm

        Parameters:
        PT (int): Plain text repsented as int value
        key (int): Key to be used for encryption represented as int value

        Returns:
        c_list (list) : List of integer values of constants used to create subkeys,
                        needed for visualisation purposes
        keys (list) : List of integer values of sub-keys used for encryption,
                      needed for visualisation purposes
        CT_list (list) : List of integer values of PT for each round

        """
        
        keys, c_list = self.generateSubKeys(key)
        CT_list = list()
        for i in range(9):
            PT = self.L(self.S(self.X(PT, keys[i])))
            CT_list.append(PT)

        PT = self.X(PT, keys[-1])
        CT_list.append(PT)

        return c_list, keys, CT_list


    def decryptKuznyechik(self, CT, key):

        """ Function that encrypts given input with given key using Kuznyechik algorithm

        Parameters:
        CT (int): Cipher text repsented as int value
        key (int): Key to be used for decryption represented as int value

        Returns:
        OT_list (list) : List of integer values of CT for each round

        """

        keys, c_list = self.generateSubKeys(key)
        OT_list = list()
        for i in reversed(range(10)):
            if i == 0:
                break
            CT = self.S_inverse(self.L_inverse(self.X(CT, keys[i])))
            OT_list.append(CT)

        CT = self.X(CT, keys[0])
        OT_list.append(CT)

        return OT_list


    """ 
    "Pi" and "Pi_neg" represent vectors (arrays) used for nonlinear bijective mapping
    (substitution) 
    """

    Pi = (252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250,
        218, 35, 197, 4, 77, 233, 119, 240, 219, 147, 46,
        153, 186, 23, 54, 241, 187, 20, 205, 95, 193, 249,
        24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66,
        139, 1, 142, 79, 5, 132, 2, 174, 227, 106, 143,
        160, 6, 11, 237, 152, 127, 212, 211, 31, 235, 52,
        44, 81, 234, 200, 72, 171, 242, 42, 104, 162, 253,
        58, 206, 204, 181, 112, 14, 86, 8, 12, 118, 18,
        191, 114, 19, 71, 156, 183, 93, 135, 21, 161, 150,
        41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158,
        178, 177, 50, 117, 25, 61, 255, 53, 138, 126, 109,
        84, 198, 128, 195, 189, 13, 87, 223, 245, 36, 169,
        62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185,
        3, 224, 15, 236, 222, 122, 148, 176, 188, 220, 232,
        40, 80, 78, 51, 10, 74, 167, 151, 96, 115, 30,
        0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65,
        173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165,
        125, 105, 213, 149, 59, 7, 88, 179, 64, 134, 172,
        29, 247, 48, 55, 107, 228, 136, 217, 231, 137, 225,
        27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144,
        202, 216, 133, 97, 32, 113, 103, 164, 45, 43, 9,
        91, 203, 155, 37, 208, 190, 229, 108, 82, 89, 166,
        116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57,
        75, 99, 182)

    Pi_neg = (165, 45, 50, 143, 14, 48, 56, 192, 84, 230, 158,
            57, 85, 126, 82, 145, 100, 3, 87, 90, 28, 96,
            7, 24, 33, 114, 168, 209, 41, 198, 164, 63, 224,
            39, 141, 12, 130, 234, 174, 180, 154, 99, 73, 229,
            66, 228, 21, 183, 200, 6, 112, 157, 65, 117, 25,
            201, 170, 252, 77, 191, 42, 115, 132, 213, 195, 175,
            43, 134, 167, 177, 178, 91, 70, 211, 159, 253, 212,
            15, 156, 47, 155, 67, 239, 217, 121, 182, 83, 127,
            193, 240, 35, 231, 37, 94, 181, 30, 162, 223, 166,
            254, 172, 34, 249, 226, 74, 188, 53, 202, 238, 120,
            5, 107, 81, 225, 89, 163, 242, 113, 86, 17, 106,
            137, 148, 101, 140, 187, 119, 60, 123, 40, 171, 210,
            49, 222, 196, 95, 204, 207, 118, 44, 184, 216, 46,
            54, 219, 105, 179, 20, 149, 190, 98, 161, 59, 22,
            102, 233, 92, 108, 109, 173, 55, 97, 75, 185, 227,
            186, 241, 160, 133, 131, 218, 71, 197, 176, 51, 250,
            150, 111, 110, 194, 246, 80, 255, 93, 169, 142, 23,
            27, 151, 125, 236, 88, 247, 31, 251, 124, 9, 13,
            122, 103, 69, 135, 220, 232, 79, 29, 78, 4, 235,
            248, 243, 62, 61, 189, 138, 136, 221, 205, 11, 19,
            152, 2, 147, 128, 144, 208, 36, 52, 203, 237, 244,
            206, 153, 16, 68, 64, 146, 58, 1, 38, 18, 26,
            72, 104, 245, 129, 139, 199, 214, 32, 10, 8, 0,
            76, 215, 116)