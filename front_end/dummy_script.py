from socket import *
from json import dumps , loads
from util import *
import protocol as p
import sys


method_dict = {
    # "log_in" : _log_in,
    "log_out" : _log_out,
    # "sample_players"  : _smp_players,
    # "create_match" : _create_match,
    # "join_match" : _join_match,
    # "push_play" : _push_play,
    # "check_mstate" : _check_mstate,
}

pvtk , pubk = generate_rsa_keys()
if __name__ == "__main__":
    
    player_id = sys.argv[ 1 ]
    p.log_in( player_id , pubk )

    while True:
        nxt_request = input( ">>>")
        if not nxt_request:
            continue

        req_fields = nxt_request.split(_)

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
