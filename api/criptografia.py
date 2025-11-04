import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

KEY = b"1234567890123456"

def encrypt(texto):
    texto_bytes = texto.encode('utf-8')
    texto_padded = pad(texto_bytes, AES.block_size)
    cipher = AES.new(KEY, AES.MODE_ECB)
    criptografado = cipher.encrypt(texto_padded)
    return base64.b64encode(criptografado).decode('utf-8')
