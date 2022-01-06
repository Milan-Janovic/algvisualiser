function validateCamellia() 
{
    keyLength = document.getElementById("keyLength");
    key = document.getElementById("key");
    message = document.getElementById("message");

    keyLengthValue = parseInt(keyLength.value);
    key = key.value;
    keyLengthBits = (key.length) * 8;
    messageLengthBits = (message.value.length) * 8;

    if(keyLengthBits == 256)
    {
        keyLengthSplit = key.split("");
        keyL = "";
        keyR = "";

        for(i = 0; i < (key.length / 2); i++)
        {
            keyL = keyL.concat(keyLengthSplit[i]);
            keyR = keyR.concat(keyLengthSplit[i+16]);
        }

        if(keyL == keyR)
        {
            alert("Key cannot consist of two same halves!");
            return false;
        }
    }

    if(keyLengthValue != 128 && keyLengthValue != 192 && keyLengthValue != 256)
    {
        alert("Key length can only be 128, 192 or 256 bits !!!");
        return false;

    }
    else if(keyLengthValue == 128 & keyLengthBits != 128)
    {
        alert("Please enter 128 bits long key.");
        return false;
    }
    else if(keyLengthValue == 192 & keyLengthBits != 192)
    {
        alert("Please enter 192 bits long key.");
        return false;
    }
    else if(keyLengthValue == 256 & keyLengthBits != 256)
    {
        alert("Please enter 256 bits long key.");
        return false;
    }
    else
    {
        return true;
    }
}

function validateChaChaKuznyechik() {
    key = document.getElementById("key");
    message = document.getElementById("message");

    key = key.value;
    keyLengthBits = (key.length) * 8;

    if(keyLengthBits < 256)
    {
        alert("Please enter 256 bits long key.");
        return false;
    }
}