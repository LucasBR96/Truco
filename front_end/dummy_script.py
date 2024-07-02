from socket import *
from json import dumps , loads
from util import *
from protocol import fe_protocol as player
import sys

a_pvtk , a_pubk = generate_rsa_keys()
alice = player( "alice" , a_pubk , a_pvtk )
alice.log_in()
alice.create_match()

b_pvtk , b_pubk = generate_rsa_keys()
bob = player( "bob" , b_pubk , b_pvtk )
bob.log_in()
bob.join_match( 0 )

#     encoded_arg = arg.encode()
#     print( f"encoded input: { encoded_arg }" )

#     HOST = "127.0.0.1"
#     PORT = 12000  # The port used by the server
#     with socket(AF_INET, SOCK_STREAM) as s:
#         s.connect((HOST, PORT))
#         s.sendall(encoded_arg)
#         data = s.recv(1024)
    

#     decoded_response = loads( data )
#     print( f"encoded output: { data }" )
#     print( f"decoded output: { decoded_response }" )
