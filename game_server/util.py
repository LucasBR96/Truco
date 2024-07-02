import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as rsa_cipher
from Crypto.Signature import PKCS1_PSS as pss
from Crypto.Hash import SHA256
# basic decoding ------------------------------------------

def hex2str( msg : str):
    return bytes.fromhex( msg[ 2: ] )

def str2hex( msg : str):
    return "0x" + str.encode( "utf-8" ).hex()

# hashing ----------------------------------------------
def hex_hash( msg : str ):

    hash_val = hash( msg )
    return hex( hash_val )[ 2: ]

# AS criptography: --------------------------------------

def generate_rsa_keys( ):

    private_obj = RSA.generate( 1024 )
    private_str = private_obj.export_key( "DER" ).hex()

    public_obj  = private_obj.public_key()
    public_str  = public_obj.export_key( "DER" ).hex()

    return private_str , public_str

def rsa_encode( entry_string : str , k_val : str ) -> str:
    
    key_obj = RSA.import_key( bytes.fromhex( k_val ) )
    cipher_obj = rsa_cipher.new( key_obj )
    encrypted_str = cipher_obj.encrypt( entry_string.encode() )
    return encrypted_str.hex()

def rsa_decode( encoded_string : str, k_val : str ) -> str:

    key_obj = RSA.import_key( bytes.fromhex( k_val ) )
    cipher_obj = rsa_cipher.new( key_obj )
    decoded_str = cipher_obj.decrypt( bytes.fromhex( encoded_string ) )
    return decoded_str.decode()

def rsa_signature( entry_string : str , k_val : str ):
    
    key_obj = RSA.import_key( bytes.fromhex( k_val ) )
    sign_object = pss.new( key_obj )
    hash_obj = SHA256.new( entry_string.encode() )
    return sign_object.sign( hash_obj ).hex()
    

def verify_signature( sign : str , entry_string : str , k_val ):
    
    key_obj = RSA.import_key( bytes.fromhex( k_val ) )
    sign_object = pss.new( key_obj )
    hash_obj = SHA256.new( entry_string.encode() )
    
    return sign_object.verify(hash_obj , bytes.fromhex( sign ) )