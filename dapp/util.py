# import Crypto
# from Crypto.PublicKey import RSA

# basic decoding ------------------------------------------

def hex2str( msg : str):
    return bytes.fromhex( msg[ 2: ] )

def str2hex( msg : str):
    return "0x" + str.encode( "utf-8" ).hex()


# AS criptography:

def rsa_encode( entry_string : str , k_val : bytes ) -> str:
    return ""