from . import Camellia
from . import helperFunctions

class Camellia192_256(Camellia.CamelliaBase):

    def switchNullsAndOnes(self, numberToBeSwitched):

        """ Function that switches nulls to ones and vice versa in binary string

        Parameters:
        numberToBeSwitched (string): Number to have it's binary values switched represented as binary string

        Returns:
        string : The input value after it's binary values were switched

        """

        numberToBeSwitched = list(numberToBeSwitched)
        for i in range(len(numberToBeSwitched)):
            if numberToBeSwitched[i] == "0":
                numberToBeSwitched[i] = "1"
            else:
                numberToBeSwitched[i] = "0"
        return ''.join(numberToBeSwitched)


    def generateKaKb192_256Key(self, Key):

        """ Function that creates 'Ka' & 'Kb' subkeys needed for encryption

        Parameters:
        Key (string): Key given for encryption, represented as 192 or 256 bit long binary string      
        
        
        Returns:
        Ka (string) : 'Ka' subkey, represented as 128 bit long binary string
        Kb (string) : 'Kb' subkey, represented as 128 bit long binary string
        KLLs (list) : List of 2 integer values of left part of 'Key' in chosen iterations,
                      needed for visualisation purposes
        KLRs (list) : List of 2 integer values of right part of 'Key' in chosen iterations,
                      needed for visualisation purposes

        """

        constants = self.constants
        KLLs = []
        KLRs = []

        if(len(Key) == 192):
            KeyL = Key[:128]
            KeyLBegining = KeyL
            KeyRRtemp = self.switchNullsAndOnes(Key[128:])
            KeyR = Key[128:] + KeyRRtemp
            
        if(len(Key) == 256):
            KeyL = Key[:128]
            KeyLBegining = KeyL
            KeyR = Key[128:]
            
        
        KeyL = bin(int(KeyL,2) ^ int(KeyR,2))[2:]
        KeyLL = KeyL[:64]
        KeyLR = KeyL[64:]
        KLLs.append(int(KeyLL,2))
        KLRs.append(int(KeyLR,2))
        
        for i in range(2):
            KeyTemp = int(self.fFunction(KeyLL, constants[i]),2) ^ int(KeyLR,2)
            KeyLR = KeyLL
            KeyLL = helperFunctions.pad(bin(KeyTemp)[2:],64)
            
        KeyL = KeyLL + KeyLR   
        KeyL = bin(int(KeyL,2) ^ int(KeyLBegining,2))[2:]
        KeyLL = KeyL[:64]
        KeyLR = KeyL[64:]
        
        for i in range(2):
            KeyTemp = int(self.fFunction(KeyLL, constants[i+2]),2) ^ int(KeyLR,2)
            KeyLR = KeyLL
            KeyLL = helperFunctions.pad(bin(KeyTemp)[2:],64)
        
        Ka = KeyLL + KeyLR
        
        KeyR = bin(int(KeyR,2) ^ int(Ka,2))[2:]
        KeyRL = KeyR[:64]
        KeyRR = KeyR[64:]
        KLLs.append(int(KeyRL,2))
        KLRs.append(int(KeyRR,2))
        
        for i in range(2):
            KeyTemp = int(self.fFunction(KeyRL, constants[i+4]),2) ^ int(KeyRR,2)
            KeyRR = KeyRL
            KeyRL = helperFunctions.pad(bin(KeyTemp)[2:],64)
            
        Kb = KeyRL + KeyRR

        return Ka, Kb, KLLs, KLRs


    def generateSubKeys192_256(self, Key, Ka, Kb):
                                
        """ Function that creates subkey needed for encryption from given 192 or 256 bit long key and
            previously generated 'Ka' & 'Kb' subkey

        Parameters:
        Key (string): Key given for encryption, represented as 192 or 256 bit long binary string       
        Ka (string): 'Ka' subkey, represented as 128 bit long binary string     
        Kb (string): 'Kb' subkey, represented as 128 bit long binary string
        
        
        Returns:
        kw (list) : List of four 64-bit long binary strings, each representing one of 'kw' subkeys
        kl (list) : List of six 64-bit long binary strings, each representing one of 'kl' subkeys
        k (list) : List of twentyfour 64-bit long binary strings, each representing one of 'k' subkeys

        """

        if(len(Key) == 192):
            KeyL = Key[:128]
            KeyRRtemp = self.switchNullsAndOnes(Key[128:])
            KeyR = Key[128:] + KeyRRtemp
        
        if(len(Key) == 256):
            KeyL = Key[:128]
            KeyR = Key[128:]
        
        
        kw = [KeyL[:64], KeyL[64:],bin(helperFunctions.rotateLeft(Kb[:64],64,111))[2:],bin(helperFunctions.rotateLeft(Kb[64:],64,111))[2:]]
        kl = [bin(helperFunctions.rotateLeft(KeyR[:64],64,30))[2:], bin(helperFunctions.rotateLeft(KeyR[64:],64,30))[2:], bin(helperFunctions.rotateLeft(KeyL[:64],64,60))[2:], bin(helperFunctions.rotateLeft(KeyL[64:],64,60))[2:], bin(helperFunctions.rotateLeft(Ka[:64],64,77))[2:], bin(helperFunctions.rotateLeft(Ka[64:],64,77))[2:]]
        k = []
        
        for i in range(4):
            kw[i] = helperFunctions.pad(kw[i],64)
            kl[i] = helperFunctions.pad(kl[i],64)
        
        
        for i in range(24):
            if i == 0 : k.append(Kb[:64])
            if i == 1 : k.append(Kb[64:])
            if i == 2 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(KeyR[:64],64,15))[2:],64))
            if i == 3 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(KeyR[64:],64,15))[2:],64))
            if i == 4 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[:64],64,15))[2:],64))
            if i == 5 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[64:],64,15))[2:],64))
            
            if i == 6 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Kb[:64],64,30))[2:],64))
            if i == 7 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Kb[64:],64,30))[2:],64))
            if i == 8 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(KeyL[:64],64,45))[2:],64))
            if i == 9 : k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(KeyL[64:],64,45))[2:],64))
            if i == 10: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[:64],64,45))[2:],64))
            if i == 11: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[64:],64,45))[2:],64))
            
            if i == 12: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(KeyR[:64],64,60))[2:],64))
            if i == 13: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(KeyR[64:],64,60))[2:],64))
            if i == 14: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Kb[:64],64,60))[2:],64))
            if i == 15: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Kb[64:],64,60))[2:],64))
            if i == 16: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(KeyL[:64],64,77))[2:],64))
            if i == 17: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(KeyL[64:],64,77))[2:],64))
            
            if i == 18: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(KeyR[:64],64,94))[2:],64))
            if i == 19: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(KeyR[64:],64,94))[2:],64))
            if i == 20: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[:64],64,94))[2:],64))
            if i == 21: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(Ka[64:],64,94))[2:],64))
            if i == 22: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(KeyL[:64],64,111))[2:],64))
            if i == 23: k.append(helperFunctions.pad(bin(helperFunctions.rotateLeft(KeyL[64:],64,111))[2:],64))

        return kw, kl, k


    def encryptCamellia192_256(self, PT, kw, kl, k):

        """ Function that encrypts given input with given key using Camellia algorithm for 192 or 256-bit long key

        Parameters:
        PT (string): Plain text repsented as binary string
        kw (list) : List of four 64-bit long binary strings, each representing one of 'kw' subkeys
        kl (list) : List of four 64-bit long binary strings, each representing one of 'kl' subkeys
        k (list) : List of eighteen 64-bit long binary strings, each representing one of 'k' subkeys

        Returns:
        (''.join(PTL +  PTR)) (string) : CT represented as binary string
        PTL_init (string) : Initial value of left part of PT, needed for visualisation purposes
        PTR_init (string) : Initial value of right part of PT, needed for visualisation purposes
        PTRs (list) : List of 2 integer values of right part of PT after 6th and 24th round,
                      needed for visualisation purposes
        PTLs (list) : List of 2 integer values of left part of PT after 6th and 24th round,
                      needed for visualisation purposes

        """

        PTL = helperFunctions.pad(bin(int(PT[:64],2) ^ int(kw[0],2))[2:],64)   
        PTR = helperFunctions.pad(bin(int(PT[64:],2) ^ int(kw[1],2))[2:],64)
        PTL_init = PTL
        PTR_init = PTR
        PTLs = []
        PTRs = []
                        
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
            
        PTL = self.flFunction(PTL,kl[4])
        PTR = self.flminusFunction(PTR,kl[5])
        
        for i in range(6):
            PTtemp = int(self.fFunction(PTL, int(k[i+18],2)),2) ^ int(PTR,2)
            PTR = PTL
            PTL = helperFunctions.pad(bin(PTtemp)[2:],64)  

        PTLs.append(int(PTL,2))
        PTRs.append(int(PTR,2))

        PTL, PTR = PTR, PTL  
        
        PTL = helperFunctions.pad(bin(int(PTL,2) ^ int(kw[2],2))[2:],64)
        PTR = helperFunctions.pad(bin(int(PTR,2) ^ int(kw[3],2))[2:],64)

        return ''.join(PTL +  PTR), PTL_init, PTR_init, PTLs, PTRs


    def decryptCamellia192_256(self, PT, kw, kl, k):
                        
        """ Function that decrypts given input with given key using Camellia algorithm for 192 or 256-bit long key

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
        PTRs (list) : List of 2 integer values of right part of PT after 24th round before and after being XORed with
                      corresponding 'kw' subkey, needed for visualisation purposes
        PTLs (list) : List of 2 integer values of left part of PT after 24th round before and after being XORed with
                      corresponding 'kw' subkey, needed for visualisation purposes
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
                
                    
        PTL = self.flFunction(PTL,kl[5])  
        PTR = self.flminusFunction(PTR,kl[4])
        
        
        for i in range(6):
            PTtemp = int(self.fFunction(PTL, int(k[i+6],2)),2) ^ int(PTR,2)
            PTR = PTL
            PTL = helperFunctions.pad(bin(PTtemp)[2:],64)
            
                    
        PTL = self.flFunction(PTL,kl[3])  
        PTR = self.flminusFunction(PTR,kl[2])
        
        
        for i in range(6):
            PTtemp = int(self.fFunction(PTL, int(k[i+12],2)),2) ^ int(PTR,2)
            PTR = PTL
            PTL = helperFunctions.pad(bin(PTtemp)[2:],64)
            
                
        PTL = self.flFunction(PTL,kl[1])
        PTR = self.flminusFunction(PTR,kl[0])
        
        for i in range(6):
            PTtemp = int(self.fFunction(PTL, int(k[i+18],2)),2) ^ int(PTR,2)
            PTR = PTL
            PTL = helperFunctions.pad(bin(PTtemp)[2:],64)

        PTLs_decipher.append(int(PTL,2))
        PTRs_decipher.append(int(PTR,2))
            
        PTL, PTR = PTR, PTL
            
        PTL = helperFunctions.pad(bin(int(PTL,2) ^ int(kw[1],2))[2:],64)
        PTR = helperFunctions.pad(bin(int(PTR,2) ^ int(kw[0],2))[2:],64)

        PTLs_decipher.append(int(PTL,2))
        PTRs_decipher.append(int(PTR,2))
        
        return ''.join(PTL + PTR), PTL_init_decipher, PTR_init_decipher, PTLs_decipher, PTRs_decipher