"""
The following code generates a new RSA key, encrypts a unicode string, and decrypts it.
Author: Woramon P.
Date: 3/12/22
"""

# pip install pycryptodome

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

# generate a new RSA key
random_generator = Random.new().read
bits = 2048

private_key = RSA.generate(bits, random_generator)  # generate a private key
public_key = private_key.publickey()  # get a public key of this key pair

# encrypt a string, using public key
string_to_encrypt = 'test STRING 123 RSA กขค 测试'  # this is a unicode string
print(type(string_to_encrypt), "length:", len(string_to_encrypt), string_to_encrypt)

data_to_encrypt = string_to_encrypt.encode('utf-8')  # convert to bytes
cipher_rsa_public = PKCS1_OAEP.new(public_key)  # get a cipher object to perform encryption
encrypted = cipher_rsa_public.encrypt(data_to_encrypt)  # encrypt
print(type(encrypted), "length:", len(encrypted), encrypted)

# decrypt a string
cipher_rsa_private = PKCS1_OAEP.new(private_key)  # get a cipher object to perform decryption
decrypted = cipher_rsa_private.decrypt(encrypted)  # decrypt
print(type(decrypted), "length:", len(decrypted), decrypted)

decrypted_string = decrypted.decode('utf-8')  # convert to string
print(type(decrypted_string), "length:", len(decrypted_string), decrypted_string)

assert decrypted_string == string_to_encrypt
