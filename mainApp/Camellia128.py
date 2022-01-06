from . import Camellia
from . import helperFunctions

class Camellia128(Camellia.CamelliaBase):

    def generateKa128Key(self, key128):
                
        """ Function that creates 'Ka' subkey needed for encryption

        Parameters:
        key128 (string): Key given for encryption, represented as 128 bit long binary string      
        
        
        Returns:
        (KeyL + KeyR) (string) : 'Ka' subkey, represented as 128 bit long binary string
        KeyTemps (list) : List of 4 integer values (from 4 iterations) of left part of 'key128'
                          after it was put throught 'fFunction' with corresponding constant,
                          needed for visualisation purposes

        KeyTempsXORed (list) : List of 4 integer values (from 4 iterations) of left part of 'key128'
                          after it was put throught 'fFunction' with corresponding constant and XORed
                          with left part if 'key128', needed for visualisation purposes

        KeyLs (list) : List of 4 integer values (from 4 iterations) of left parts in given itterations
        KeyRs (list) : List of 4 integer values (from 4 iterations) of right parts in given itterations

        """

        constants = self.constants
        KeyL = key128[:64]
        KeyR = key128[64:]
        KeyLbegining = KeyL + KeyR
        KeyTemps = []
        KeyTempsXORed = []
        KeyRs = []
        KeyLs = []
        
        for i in range(2):
            KeyTemps.append(int(self.fFunction(KeyL, constants[i]),2))
            KeyTemp = (int(self.fFunction(KeyL, constants[i]),2) ^ int(KeyR,2))
            KeyTempsXORed.append(KeyTemp)
            KeyR = KeyL
            KeyRs.append(int(KeyR,2))
            KeyL = helperFunctions.pad(bin(KeyTemp)[2:],64)
            KeyLs.append(int(KeyL,2))


        iKey = KeyL + KeyR
        iKey = int(iKey,2) ^ int(KeyLbegining,2)
        iKey = helperFunctions.pad(bin(iKey)[2:],128)
        KeyL = iKey[:64]
        KeyR = iKey[64:]

        for i in range(2):
            KeyTemps.append(int(self.fFunction(KeyL, constants[i+2]),2))
            KeyTemp = (int(self.fFunction(KeyL, constants[i+2]),2) ^ int(KeyR,2))
            KeyTempsXORed.append(KeyTemp)
            KeyR = KeyL
            KeyRs.append(int(KeyR,2))
            KeyL = helperFunctions.pad(bin(KeyTemp)[2:],64)
            KeyLs.append(int(KeyL,2))

        return KeyL + KeyR, KeyTemps, KeyTempsXORed, KeyLs, KeyRs


    def generateSubKeys128(self, key128, Ka):
                        
        """ Function that creates subkey needed for encryption from given 128 bit long key and
            previously generated 'Ka' subkey

        Parameters:
        key128 (string): Key given for encryption, represented as 128 bit long binary string      
        Ka (string): 'Ka' subkey, represented as 128 bit long binary string     
        
        
        Returns:
        kw (list) : List of four 64-bit long binary strings, each representing one of 'kw' subkeys
        kl (list) : List of four 64-bit long binary strings, each representing one of 'kl' subkeys
        k (list) : List of eighteen 64-bit long binary strings, each representing one of 'k' subkeys

        """

        kw = [key128[:64], key128[64:],bin(helperFunctions.rotateLeft(Ka[:64],64,111))[2:],bin(helperFunctions.rotateLeft(Ka[64:],64,111))[2:]]
        kl = [bin(helperFunctions.rotateLeft(Ka[:64],64,30))[2:], bin(helperFunctions.rotateLeft(Ka[64:],64,30))[2:], bin(helperFunctions.rotateLeft(key128[:64],64,77))[2:], bin(helperFunctions.rotateLeft(key128[64:],64,77))[2:]]
        k = []
        
        
        for i in range(4):
            kw[i] = helperFunctions.pad(kw[i],64)
            kl[i] = helperFunctions.pad(kl[i],64)
        
        
        for i in range(18):
            if i == 0 : k.append(Ka[:64])
            if i == 1 : k.append(Ka[64:])
            if i == 2 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(key128[:64],64,15))[2:],64))
            if i == 3 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(key128[64:],64,15))[2:],64))
            if i == 4 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[:64],64,15))[2:],64))
            if i == 5 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[64:],64,15))[2:],64))
            
            if i == 6 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(key128[:64],64,45))[2:],64))
            if i == 7 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(key128[64:],64,45))[2:],64))
            if i == 8 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[:64],64,45))[2:],64))
            if i == 9 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(key128[64:],64,60))[2:],64))
            if i == 10: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[:64],64,60))[2:],64))
            if i == 11: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[64:],64,60))[2:],64))
            
            if i == 12: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(key128[:64],64,94))[2:],64))
            if i == 13: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(key128[64:],64,94))[2:],64))
            if i == 14: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[:64],64,94))[2:],64))
            if i == 15: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[64:],64,94))[2:],64))
            if i == 16: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(key128[:64],64,111))[2:],64))
            if i == 17: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(key128[64:],64,111))[2:],64))

        return kw, kl, k


    def encryptCamellia128(self, PT, kw, kl, k):
        
        """ Function that encrypts given input with given key using Camellia algorithm for 128-bit long key

        Parameters:
        PT (string): Plain text repsented as binary string
        kw (list) : List of four 64-bit long binary strings, each representing one of 'kw' subkeys
        kl (list) : List of four 64-bit long binary strings, each representing one of 'kl' subkeys
        k (list) : List of eighteen 64-bit long binary strings, each representing one of 'k' subkeys

        Returns:
        (''.join(PTL +  PTR)) (string) : CT represented as binary string
        PTL_init (string) : Initial value of left part of PT, needed for visualisation purposes
        PTR_init (string) : Initial value of right part of PT after being XORed with second 'kw' subkey,
                          needed for visualisation purposes
        PTRs (list) : List of 2 integer values of right part of PT, needed for visualisation purposes
        PTLs (list) : List of 2 integer values of left part of PT after 6th and 18th round,
                      needed for visualisation purposes

        """

        PTL = helperFunctions.pad(bin(int(PT[:64],2) ^ int(kw[0],2))[2:],64)   
        PTR = helperFunctions.pad(bin(int(PT[64:],2) ^ int(kw[1],2))[2:],64)
        PTL_init = PTL
        PTR_init = PTR
        PTRs = []
        PTLs = []
                
        for i in range(6):
            PTtemp = int(self.fFunction(PTL, int(k[i],2)),2) ^ int(PTR,2)
            PTR = PTL
            PTL = helperFunctions.pad(bin(PTtemp)[2:],64)
                        
        PTL = self.flFunction(PTL,kl[0])
        PTR = self.flminusFunction(PTR,kl[1])

        PTLs.append(int(PTL,2))
        PTRs.append(int(PTR,2))
            
        for i in range(6):
            PTtemp = int(self.fFunction(PTL, int(k[i+6],2)),2) ^ int(PTR,2)
            PTR = PTL
            PTL = helperFunctions.pad(bin(PTtemp)[2:],64)

        PTL = self.flFunction(PTL,kl[2])
        PTR = self.flminusFunction(PTR,kl[3])
        
        for i in range(6):
            PTtemp = int(self.fFunction(PTL, int(k[i+12],2)),2) ^ int(PTR,2)
            PTR = PTL
            PTL = helperFunctions.pad(bin(PTtemp)[2:],64)  
            
        PTLs.append(int(PTL,2))
        PTRs.append(int(PTR,2))
        PTL, PTR = PTR, PTL  
        
        PTL = helperFunctions.pad(bin(int(PTL,2) ^ int(kw[2],2))[2:],64)
        PTR = helperFunctions.pad(bin(int(PTR,2) ^ int(kw[3],2))[2:],64)

        PTL_final = PTL
        PTR_final = PTR

        return ''.join(PTL +  PTR), PTL_init, PTR_init, PTRs, PTLs


    def decryptCamellia128(self, PT, kw, kl, k):
                
        """ Function that decrypts given input with given key using Camellia algorithm for 128-bit long key

        Parameters:
        PT (string): Plain text (Cipher Text) repsented as binary string
        kw (list) : List of four 64-bit long binary strings, each representing one of 'kw' subkeys
        kl (list) : List of four 64-bit long binary strings, each representing one of 'kl' subkeys
        k (list) : List of eighteen 64-bit long binary strings, each representing one of 'k' subkeys

        Returns:
        (''.join(PTL +  PTR)) (string) : CT represented as binary string
        PTL_init_decipher (string) : Initial value of left part of PT after being XORed with third 'kw' subkey,
                                     needed for visualisation purposes
        PTL_init_decipher (string) : Initial value of right part of PT after being XORed with fourth 'kw' subkey,
                                     needed for visualisation purposes
        PTRs_decipher (list) : List of 2 integer values of right part of PT after 6th and 18th round,
                               needed for visualisation purposes
        PTLs_decipher (list) : List of 2 integer values of left part of PT after 6th and 18th round,
                               needed for visualisation purposes
        PTL_final_decipher (string) : Initial value of left part of PT after being XORed with first 'kw' subkey,
                                      needed for visualisation purposes
        PTR_final_decipher (string) : Initial value of right part of PT after being XORed with second 'kw' subkey,
                                      needed for visualisation purposes

        """

        PTL = helperFunctions.pad(bin(int(PT[:64],2) ^ int(kw[2],2))[2:],64)   
        PTR = helperFunctions.pad(bin(int(PT[64:],2) ^ int(kw[3],2))[2:],64)
        PTL_init_decipher = PTL
        PTR_init_decipher = PTR
        PTLs_decipher = []
        PTRs_decipher = []
        k = k[::-1]
        
        for i in range(6):
            PTtemp = int(self.fFunction(PTL, int(k[i],2)),2) ^ int(PTR,2)
            PTR = PTL
            PTL = helperFunctions.pad(bin(PTtemp)[2:],64)    
                    
        PTL = self.flFunction(PTL,kl[3])  
        PTR = self.flminusFunction(PTR,kl[2])
        
        for i in range(6):
            PTtemp = int(self.fFunction(PTL, int(k[i+6],2)),2) ^ int(PTR,2)
            PTR = PTL
            PTL = helperFunctions.pad(bin(PTtemp)[2:],64)
            
                
        PTL = self.flFunction(PTL,kl[1])
        PTR = self.flminusFunction(PTR,kl[0])
        
        for i in range(6):
            PTtemp = int(self.fFunction(PTL, int(k[i+12],2)),2) ^ int(PTR,2)
            PTR = PTL
            PTL = helperFunctions.pad(bin(PTtemp)[2:],64)

        PTLs_decipher.append(int(PTL,2))
        PTRs_decipher.append(int(PTR,2))
            
        PTL, PTR = PTR, PTL

        PTLs_decipher.append(int(PTL,2))
        PTRs_decipher.append(int(PTR,2))
            
        PTL = helperFunctions.pad(bin(int(PTL,2) ^ int(kw[0],2))[2:],64)
        PTR = helperFunctions.pad(bin(int(PTR,2) ^ int(kw[1],2))[2:],64)

        PTL_final_decipher = PTL
        PTR_final_decipher = PTR
     
        return ''.join(PTL + PTR), PTL_init_decipher , PTR_init_decipher, PTLs_decipher, PTRs_decipher, PTL_final_decipher, PTR_final_decipher