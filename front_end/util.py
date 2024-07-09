# import Crypto
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP as rsa_cipher
# from Crypto.Signature import PKCS1_PSS as pss
# from Crypto.Hash import SHA256

from random import choices

from hashlib import sha224
# basic decoding ------------------------------------------

def hex2str( msg : str):
    return bytes.fromhex( msg[ 2: ] )

def str2hex( msg : str):
    return "0x" + msg.encode( "utf-8" ).hex()

# hashing ----------------------------------------------
def hex_hash( msg : str ):

    hash_val = sha224( msg.encode() ).hexdigest()
    return hash_val[ 0 : 25 ]

def make_signature( msg : str , cipher_key : str ):

    hash_str = hex_hash( msg )
    return str_encode( hash_str , cipher_key )

def verify_signature( msg : str , sign : str , cipher_key):

    expected_msg = str_decode( sign , cipher_key )
    return hex_hash( msg ) == expected_msg

def generate_128bit_key():

    chars = "0123456789abcdef"
    hex_form = ''.join( choices( chars , k = 32 ) )
    return '0x' + hex_form

def build_rotor( cipher_key : bytes ):

    i , j = 0 , 0
    rot_1 = cipher_key[ : 8 ]
    rot_2 = cipher_key[ 8 : ]

    while True:

        a = rot_1[ i ]
        b = rot_2[ j ]
        yield a ^ b

        i = ( i + 1 )%8
        if i: continue
        j = ( j + 1 )%8

def byte_encode( msg : bytes, cipher_key : bytes ):

    rotor = build_rotor( cipher_key )
    s = b''
    for msg_byte in msg:
        key_byte = next( rotor )
        
        x = msg_byte ^ key_byte
        s += x.to_bytes( 1 , 'big' )
    
    return s

def str_encode( msg : str, cipher_key : str ):

    '''
    input:
        msg in str form
        cipher_key in hex form
    
    output
        encoded msg in hex form
    '''
    encoded = byte_encode(
        msg.encode(), hex2str( cipher_key )
    )

    return '0x' + encoded.hex()

def str_decode( msg : str , cipher_key : str ):

    '''
    input:
        encoded msg in hex form
        cipher_key in hex form
    
    output
        msg in str form
    '''

    return byte_encode(
        hex2str( msg ) , hex2str( cipher_key )
    ).decode()
