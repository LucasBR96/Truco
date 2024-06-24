from socket import *
from json import dumps , loads
from util import *

import sys

if __name__ == "__main__":
    
    arg = sys.argv[ 1 ]
    print( f"raw input: { arg }" )

    encoded_arg = arg.encode()
    print( f"encoded input: { encoded_arg }" )

    HOST = "127.0.0.1"
    PORT = 12000  # The port used by the server
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(encoded_arg)
        data = s.recv(1024)
    

    decoded_response = loads( data )
    print( f"encoded output: { data }" )
    print( f"decoded output: { decoded_response }" )
