# import Crypto
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP as rsa_cipher
# from Crypto.Signature import PKCS1_PSS as pss
# from Crypto.Hash import SHA256

from hashlib import sha224
# basic decoding ------------------------------------------

def hex2str( msg : str):
    return bytes.fromhex( msg[ 2: ] )

def str2hex( msg : str):
    return "0x" + str.encode( "utf-8" ).hex()

# hashing ----------------------------------------------
def hex_hash( msg : str ):

    hash_val = sha224( msg.encode() ).hexdigest()
    return hash_val[ 0 : 15 ]

def make_signature( msg : str , previous_sign = None ):

    if previous_sign is None:
        previous_sign = ''
    msg = msg + previous_sign
    return hex_hash( msg )

def verify_signature( msg : str , sign , previous_sign = None ):

    expected_sign = make_signature( msg , previous_sign )
    return sign == expected_sign
