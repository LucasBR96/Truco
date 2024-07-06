from socket import *
from json import dumps , loads
from util import *
from protocol import fe_protocol as player
import sys

def init_players():
    # a_pvtk , a_pubk = generate_rsa_keys()
    alice = player( "alice" , "aaaaa" , "aaaa" )
    alice.log_in()
    alice.create_match()

    # b_pvtk , b_pubk = generate_rsa_keys()
    bob = player( "bob" , "bbbbbb" , "bbbbbb" )
    bob.log_in()
    bob.join_match( 0 )

    return alice , bob

def next_card( plyr_obj : player ):

    match_state = plyr_obj.match_state
    hand = match_state[ "hand" ]
    
    if not hand:
        return None
    return hand[ 0 ].split( sep = "-" )

def is_player_nxt( plyr_obj : player ):

    match_state = plyr_obj.match_state
    return match_state[ "your_turn" ]

# def is_match_over( plyr_obj : player ):
#     return plyr_obj.is_match_over

def simulate_match( alice : player , bob : player ):

    move_count = 0
    while True:

        alice.check_mstate()
        bob.check_mstate()
        match_state = alice.match_state

        winner = match_state.get( 'winner' , None )
        if not( winner is None ):
            break

        plr_obj = alice
        if is_player_nxt( bob ):
            plr_obj = bob
        
        card = next_card( plr_obj )
        if card is None: continue

        val , rank = card
        plr_obj.push_play( val , rank )
        move_count += 1

        print(
            f"{move_count-1} player {plr_obj.player_id} pushes {val}-{rank}"
        )

        if move_count%6: continue

    
    return alice.report_match()

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
