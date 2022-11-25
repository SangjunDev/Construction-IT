from django.shortcuts import render
import base64
import hashlib
from Crypto.Cipher import AES
import json

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[0:-ord(s[-1])]


BLOCK_SIZE = 16
pad = (lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE).encode())
unpad = (lambda s: s[:-ord(s[len(s)-1:])])

class AESCipher(object):
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()
    
    def encrypt(self, message):
        message = message.encode()
        raw = pad(message)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode('utf8'))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')
    
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode('utf8'))
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')
    
    def __iv(self):
        return chr(0) * 16
    

def about(request):
    key = '!01234!5678998765!43210!'
    data  = 'Test'
    aes  = AESCipher(key)
    encrypt  = aes.encrypt(data)
    decrypt  = aes.decrypt(encrypt)
    etcdict= {
        #'key' : key,
        #'key 1': encrypt,
        #'key 2': decrypt,
        'host' : 'cnditest.kro.kr',
        'port' : 9001,
        'userName' : 'user',
        'userPassword' : '1234'
    }
    
    etcjson = json.dumps(etcdict)
    
    return render(request, 'access/about.html', {'etcjson' : etcjson})