"""
    The following code generates a new AES128 key, encrypts a unicode string, and decrypts it.
    Author: Woramon P.
    Date: 3/12/22
"""

# pip install pycryptodome

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# generate a new AES128 key (16 bytes)
AES_bytes = 16
secret_key = get_random_bytes(AES_bytes)
cipher = AES.new(secret_key, AES.MODE_ECB)  # ECB is not strong

# encrypt a string
string_to_encrypt = 'test STRING 123 AES กขค 测试'  # this is a unicode string
print(type(string_to_encrypt), "length:", len(string_to_encrypt), string_to_encrypt)

data_to_encrypt = pad(string_to_encrypt.encode('utf-8'), AES_bytes)  # convert to bytes and pad
encrypted = cipher.encrypt(data_to_encrypt)
print(type(encrypted), "length:", len(encrypted), encrypted)

# decrypt a string
decrypted = cipher.decrypt(encrypted)
print(type(decrypted), "length:", len(decrypted), decrypted)

decrypted_string = unpad(decrypted, AES_bytes).decode('utf-8')  # unpad and convert to string
print(type(decrypted_string), "length:", len(decrypted_string), decrypted_string)

assert decrypted_string == string_to_encrypt
