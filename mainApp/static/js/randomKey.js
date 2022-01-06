function getRandomKey(length) {
    var randomChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var result = '';
    for ( var i = 0; i < length; i++ ) {
        result += randomChars.charAt(Math.floor(Math.random() * randomChars.length));
    }

    var keyTextBox = document.getElementById('key')
    keyTextBox.value = result;
}

function getRandomKeyCamellia() {
    var keyLength = document.getElementById('keyLength').value
    var length = 0

    if (keyLength == '128') 
    {
        length = 16;
    }
    else if (keyLength == '192')
    {
        length = 24;
    }
    else if (keyLength == '256')
    {
        length = 32;
    }
    else
    {
        length = 0;
        alert("Incorrect key length!")
    }

    var randomChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var result = '';
    for ( var i = 0; i < length; i++ ) {
        result += randomChars.charAt(Math.floor(Math.random() * randomChars.length));
    }

    var keyTextBox = document.getElementById('key')
    keyTextBox.value = result;
}