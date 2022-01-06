from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import Camellia128
from . import Camellia192_256
from . import ChaCha20
from . import Kuznyechik
from . import helperFunctions
import random

def index(request):
    return render(request, 'index.html', {})

def camellia_input(request):
    return render(request, 'camellia_input.html', {})

def camellia(request):

    if request.method == "POST":

        postContent = {
            "keyLenght" : request.POST.get('keyLength'),
            "Key" : request.POST.get('Key'),
            "message" : request.POST.get('message')
        }

        if(postContent.get("keyLenght") == "128"):

            camellia128 = Camellia128.Camellia128(postContent.get("keyLenght"),postContent.get("Key"),postContent.get("message"))
            message, key = helperFunctions.processInput(postContent.get("Key"), postContent.get("message"))

            key128 = helperFunctions.pad(key, 128)
            PT = helperFunctions.pad(message,128)

            Ka, KeyTemps, KeyTempsXORed, KeyLs, KeyRs = camellia128.generateKa128Key(key128)
            kw, kl, k = camellia128.generateSubKeys128(key128, Ka)
            Cipher, PTL_init, PTR_init, PTRs, PTLs = camellia128.encryptCamellia128(PT, kw, kl, k)
            Cipher_ASCII = helperFunctions.getCharacters(Cipher)
            PtDecipher, PTL_init_decipher, PTR_init_decipher, PTLs_decipher, PTRs_decipher, PTL_final_decipher, PTR_final_decipher  = camellia128.decryptCamellia128(Cipher, kw, kl, k)
            PtDecipher_ASCII = helperFunctions.getCharacters(PtDecipher)

            for i in range(len(kw)):
                kw[i] = int(kw[i],2)
                kl[i] = int(kl[i],2)

            for i in range(len(k)):
                k[i] = int(k[i],2)

            content = {
                "keyLenght" : request.POST.get('keyLength'),
                "key" : request.POST.get('Key'),
                "key_binary" : int(key,2),
                "message" : request.POST.get('message'),
                "message_binary" : int(message,2),
                "keyL" : int(key128[:64],2),
                "keyR" : int(key128[64:],2),
                "keyTemps": KeyTemps,
                "keyTempsXORed": KeyTempsXORed,
                "keyLs": KeyLs,
                "keyRs": KeyRs,
                "Ka" : int(Ka,2),
                "KaBinary" : helperFunctions.pad(bin(int(Ka,2))[2:],128),
                "kw" : kw,
                "kl" : kl,
                "k" : k,
                "PT" : int(PT,2),
                "PTL_init" : int(PTL_init,2),
                "PTR_init" : int(PTR_init,2),
                "PTLs6" : PTLs[0],
                "PTRs6" : PTRs[0],
                "PTLs18" : PTLs[1],
                "PTRs18" : PTRs[1],
                "CT_final" : int(Cipher,2),
                "CT_final_ASCII" : Cipher_ASCII,
                "PTL_init_decipher" : int(PTL_init_decipher,2),
                "PTR_init_decipher" : int(PTR_init_decipher,2),
                "PTLs1_decipher" : PTLs_decipher[0],
                "PTRs1_decipher" : PTRs_decipher[0], 
                "PTLs1_swap_decipher" : PTLs_decipher[1],
                "PTRs1_swap_decipher" : PTRs_decipher[1], 
                "PTL_final_decipher" : int(PTL_final_decipher,2),
                "PTR_final_decipher" : int(PTR_final_decipher,2),
                "PT_final" : int(PtDecipher,2),
                "PT_final_ASCII" : PtDecipher_ASCII
            }
            return render(request, 'camellia_128.html', content)
    
        if(postContent.get("keyLenght") == "192" or postContent.get("keyLenght") == "256"):

            camellia192256 = Camellia192_256.Camellia192_256(postContent.get("keyLenght"),postContent.get("Key"),postContent.get("message"))
            message, key = helperFunctions.processInput(postContent.get("Key"), postContent.get("message"))

            if(postContent.get("keyLenght") == "192"):
                key192_256 = helperFunctions.pad(key,192)
            if(postContent.get("keyLenght") == "256"):
                key192_256 = helperFunctions.pad(key,256)
        
            PT = helperFunctions.pad(message,128)

            Ka, Kb, KLLs, KLRs = camellia192256.generateKaKb192_256Key(key192_256)
            kw, kl, k = camellia192256.generateSubKeys192_256(key192_256, Ka, Kb)
            Cipher, PTL_init, PTR_init, PTLs, PTRs = camellia192256.encryptCamellia192_256(PT, kw, kl, k)
            Cipher_ASCII = helperFunctions.getCharacters(Cipher)
            PtDecipher, PTL_init_decipher, PTR_init_decipher, PTLs_decipher, PTRs_decipher = camellia192256.decryptCamellia192_256(Cipher, kw, kl, k)
            PtDecipher_ASCII = helperFunctions.getCharacters(PtDecipher)

            for i in range(len(kw)):
                kw[i] = int(kw[i],2)

            for i in range(len(kl)):
                kl[i] = int(kl[i],2)

            for i in range(len(k)):
                k[i] = int(k[i],2)

            content = {
                "keyLenght" : request.POST.get('keyLength'),
                "key" : request.POST.get('Key'),
                "key_binary" : str(int(key192_256,2))[:50] + ".....",
                "message" : request.POST.get('message'),
                "message_binary" : int(message,2),
                "KLL1" : KLLs[0],
                "KLR1" : KLRs[0],
                "Ka" : int(Ka,2),
                "KLL2" : KLLs[1],
                "KLR2" : KLRs[1],
                "Kb" : int(Kb,2),
                "kw" : kw,
                "k" : k,
                "kl" : kl,
                "PT" : int(PT,2),
                "PTL_init" : int(PTL_init,2),
                "PTR_init" : int(PTR_init,2),
                "PTLs6" : PTLs[0],
                "PTRs6" : PTRs[0],
                "PTLs24" : PTLs[1],
                "PTRs18" : PTRs[1],
                "CT_final" : int(Cipher,2),
                "CT_final_ASCII" : Cipher_ASCII,
                "PTL_init_decipher" : int(PTL_init_decipher,2),
                "PTR_init_decipher" : int(PTR_init_decipher,2),
                "PTLs1_decipher" : PTLs_decipher[0],
                "PTRs1_decipher" : PTRs_decipher[0],
                "PTL_final_decipher" : PTLs_decipher[1],
                "PTR_final_decipher" : PTRs_decipher[1],
                "PT_final" : int(PtDecipher,2),
                "PT_final_ASCII" : PtDecipher_ASCII
            }
            return render(request, 'camellia_192_256.html', content)

    else:
        return render(request, 'camellia_input.html', {})

def chacha20_input(request):
    return render(request, 'chacha20_input.html', {})

def chacha20(request):
    postContent = {
        "Key" : request.POST.get('Key'),
        "message" : request.POST.get('message')
    }

    chacha = ChaCha20.ChaCha20(request.POST.get('Key'), request.POST.get('message'))
  
    message, key = helperFunctions.processInput(postContent.get("Key"), postContent.get("message"))
    constant = chacha.processConstant()
    constant_initial = ''.join(constant)
    constant_integer = [int(x,2) for x in constant]
    iconstant = chacha.generateConstantParts(constant)
    ikey = chacha.splitKey(key)
    nonce = chacha.getRandomNumber96Bits()
    inonce = chacha.splitNonce(nonce)

    CT, matrixFlat, PT = chacha.encryptChaCha20(message, iconstant, ikey, inonce)

    CT_ASCII = helperFunctions.getCharacters(''.join(CT))
    CT_decipher, PT_decipher = chacha.decryptChaCha20(CT, iconstant, ikey, inonce)
    PT_ASCII = helperFunctions.getCharacters(''.join(CT_decipher))

    msg = request.POST.get('message')
    if (len(msg) > 50):
        msg = msg[:50] + "......"

    msg_int = str(int(message,2))
    if (len(msg_int) > 50):
        msg_int = msg_int[:50] + "......"
    
    content = {
        "key" : request.POST.get('Key'),
        "key_binary" : str(int(key,2))[:50] + "......",
        "message" : msg,
        "message_binary" : msg_int,
        "constant_initial" : int(constant_initial,2),
        "constant_integer" : constant_integer,
        "iconstant" : iconstant,
        "keys" : ikey,
        "nonce" : inonce,
        "matrixFinal" : matrixFlat, 
        "PT" : PT,
        "CT" : CT,
        "CT_ASCII" : CT_ASCII, 
        "PT_decipher" : PT_decipher,
        "PT_ASCII" : PT_ASCII, 
    }

    return render(request, 'chacha20.html', content)

def kuznyechik_input(request):
    return render(request, 'kuznyechik_input.html', {})

def kuznyechik(request):

    if request.method == "POST":

        postContent = { 
            "Key" : request.POST.get('Key'),
            "message" : request.POST.get('message')
        }

        kuznyechik = Kuznyechik.Kuznyechik(request.POST.get('Key'), request.POST.get('message'))
        message, key = helperFunctions.processInput(postContent.get("Key"), postContent.get("message"))
        message_int, key_int = int(message,2), int(key,2)
        
        c_list, keys, CT_list = kuznyechik.encryptKuznyechik(message_int, key_int)
        OT_list = kuznyechik.decryptKuznyechik(CT_list[9], key_int)
     
        content = {
            "message": request.POST.get('message'), 
            "key" : request.POST.get('Key'),
            "message_int" : message_int,
            "key_int" : str(key_int)[:50] + "......",
            "c_list" : c_list,
            "keys" : keys,
            "CT_list" : CT_list,
            "OT_list" : OT_list,
            "OT" : helperFunctions.getCharactersKuznyechik(bin(OT_list[9])[2:]),
            "CT" : helperFunctions.getCharactersKuznyechik(bin(CT_list[9])[2:]),
        }

        return render(request, 'kuznyechik.html', content)
    else:
        return render(request, 'kuznyechik_input.html', {})