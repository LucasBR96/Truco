from socket import *
from json import dumps , loads
from util import *

from play import *

def log_in( player_id , pubk ):
    
    request = { "player_id" : player_id , "pubk" : pubk }
    flag , resp = send_request( "log_in" , request )
    # if flag:
    #     return "OK"
    # return resp
    return flag , resp

def log_out( player_id ):

    request = { "player_id" : player_id }
    flag , resp = send_request( "log_out" , request )
    # if flag:
    #     return "OK"
    # return resp
    return flag , resp

def create_match( player_id ):
    
    request = { "player_id" : player_id  }
    flag , resp = send_request( "create_match" , request )
    if flag:
        match_id = resp["match_id"]
        return f"OK MATCH_ID {match_id}"
    return resp
    # return flag , resp 

def join_match( player_id , match_id ):

    request = { "player_id" : player_id , "match_id" : match_id }
    flag , resp = send_request( "join_match" , request )
    if flag:
        return "OK"
    return resp

def check_mstate( player_id ):

    request = { "player_id" : player_id  }
    flag , resp = send_request( "check_mstate" , request )
    if not flag:
        return resp
    
    match_dict = resp
    
    s = f"OK" + "\n"
    for k , v in match_dict.items():
        s += "\n" + f"{k} : {v}"
    return s
    # return flag , resp

def push_play( player_id , match_id , card_val , card_rank , pvtk , mv_hist : list = [] ):

    request = { "player_id" : player_id  }
    flag , resp = send_request( "check_mstate" , request )

    last_play , last_sign = resp[ "last_mv" ] , resp[ "last_sign"] 
    if last_play is not None:
        update_mv_hist( last_play , last_sign , mv_hist )

    mv = play(
        match_id,
        resp["curr_round"],
        resp[ "turn" ],
        player_id,
        card_val,
        card_rank
    )
    request[ "match_id" ] = match_id
    request[ "play_str" ] = str( mv )

    h_str = str( mv )
    if last_sign is not None:
        h_str += last_sign
        
    sgn_str = rsa_signature( h_str , pvtk )
    request[ "sign_str" ] = sgn_str


    flag , resp = send_request("push_play" , request )
    if flag:
        update_mv_hist( str( mv ) , sgn_str , mv_hist )
        return "OK"
    return resp

def update_mv_hist( mv_str , sign_str , mv_hist : list ):

    if not mv_hist:
        mv_hist.append( ( mv_str , sign_str ) )
    
    if mv_str != mv_hist[ -1 ][ 0 ]:
        mv_hist.append( ( mv_str , sign_str ) )

def send_request( request_type , request_args ):


    request_body = {
        "method" : request_type,
        "args"   : request_args
    }

    HOST = "127.0.0.1"
    PORT = 12000  # The port used by the server
    with socket(AF_INET, SOCK_STREAM) as s:

        s.connect((HOST, PORT))
        s.sendall( dumps( request_body ).encode() )
        data = loads( s.recv(1024) )
    
    flag = ( data[ "flag" ] == "ok" )
    if flag:
        resp = data["args"]
    else:
        err_type = data[ "err_type" ]
        msg = data[ "msg" ]
        resp = f"{err_type} : {msg}"
    return flag , resp

if __name__ == "__main__":
    pvtk , pubk = generate_rsa_keys()