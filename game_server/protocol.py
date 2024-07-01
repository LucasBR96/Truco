# from game_server.match import *

import pandas as pd

from player import *
from errors import *
from match import *
from constantes import *
from play import *
from match_fsm import *
from util import *

from json import loads , dumps
import time as t
# ------------------------------------------------------------
# Jogos

# player_col = ["player_id" , "session_num" , "pubk" , "status" , "current_match" ]
# logged_players : pd.DataFrame = pd.DataFrame( [] , columns = player_col )
# logged_players.set_index( "player_id" )
make_player_df()

# match_col = [ "match_id" , "player_1", "player_2" , "status" ]
# current_matches = match
create_match_df()

def _log_in( request_msg ):

    '''
    Player connects to the server

    Request:
        { "player_id" : <playerId> , "addr": <playerIp> , "pubk" : playerPubKey }
    response:
        { flag : "ok" , args : [ player_id , session_num , timestamp ] }
    '''

    player_id = request_msg[ "player_id"]
    if is_logged( player_id ):
        raise illegalMethod( f"player {player_id} is already logged in" )
    
    # ---------------------------------
    # saving player
    pubk = request_msg[ "pubk" ]
    add_player( player_id , pubk )
    
    # ----------------------------------
    # making response
    response_dict = {
        "flag": "ok",
        "args" : {
            "player_id" : player_id,
            "timestamp" : t.time()
        }
    }

    return response_dict

def _log_out( request_msg ):

    '''
    Removes player from the server

    request:
        { "player_id" : <playerId> , "addr": <playerIp>  }
    response:
        { "flag" : "ok" , "args" : { ... } }
    '''

    # checking legallity ---------------------------------
    player_id = request_msg[ "player_id"]
    if is_logged( player_id ):
        rmv_player( player_id )
    else:
        raise illegalMethod( f"Player {player_id} already logged out.")
    
    response_dict = {
        "flag": "ok",
        "args" : {
            "player_id" : player_id,
            "timestamp" : t.time()
        }
    }

    return response_dict

def _smp_players( request_msg ):

    # checking legallity ---------------------------------
    player_id = request_msg[ "player_id"]
    if not is_logged( player_id ):
        raise illegalMethod( 'requesting player is not logged in')
    
    status_filter = request_msg.get( "status" , None )
    players = sample_players( status_filter ).to_dict()

    response_dict = {
        "flag" : "ok",
        "args" : players
    }

    return response_dict

def _create_match( request_msg ):

    ''' 
    1) Create Game
    request:
        { "player_id" : <playerId> , "addr" : PlayerAddr }
    response:
        { "flag" : ok , args : [ player_id , game_id , timestamp ]}
   '''

    # checking legallity ---------------------------------
    player_id = request_msg[ "player_id" ]
    if not is_logged( player_id ):
        raise illegalMethod( f"Player {player_id} already logged out.")
    
    # player must be idle -----------------------------------
    player_info = get_player( player_id )
    if player_info[ "status" ] != IDLE:
        raise illegalMethod( f"Player {player_id} is already active.")
    
    match_id = add_match( player_id )
    set_match( player_id , match_id )
    set_status( player_id , WAITING )

    # response
    response_payload = {
        "flag": "ok",
        "args" :{
            "match_owner" : player_id,
            "match_id"    : match_id,
            "match_start" : t.time()
        }
    }

    return response_payload

def _join_match( request_msg ):

    '''
    player joins a running game

    Request:
        { "player_id" : <playerId> , "addr" : <playerAddres> ,"game_id" : <id> }
    response:
        { "flag" : "ok" , "args": { "match_id" : match_id, "timestamp" : <logTime> } }
    '''

   # checking legallity ---------------------------------
    player_id = request_msg[ "player_id" ]
    if not is_logged( player_id ):
        raise illegalMethod( f"Player {player_id} already logged out.")
    
    # player must be idle -----------------------------------
    player_info = get_player( player_id )
    if player_info[ "status" ] != IDLE:
        raise illegalMethod( f"Player {player_id} is already active.")
    
    match_id = request_msg[ "match_id" ]
    if not match_exists( match_id ):
        raise illegalMethod( f"Match {match_id} does not exist" )
    
    match_info = get_match( match_id )
    if match_info[ "current_status" ] == PLAYING:
        raise illegalMethod( f"Match {match_id} already full" )

    join_match( match_id , player_id )
    set_match( player_id , match_id )
    set_status( player_id , PLAYING )
    set_status( match_info[ "player_1_id"] , PLAYING )

    # response
    response_payload = {
        "flag": "ok",
        "args" :{
            "match_id"    : match_id,
            "match_start" : t.time()
        }
    }

    return response_payload

def _push_play( request_msg ):

    '''
    { player_id , match_id , play_num , card_n , card_color ,  }
    '''

    match_id = request_msg[ "match_id" ]
    match_obj : match_fsm = get_match_obj( match_id )

    player_id = request_msg[ "player_id" ]
    pubk = get_player( player_id )[ "pubk" ]

    play_str = request_msg[ "play_str" ]
    play_obj = play.from_str( play_str )

    # play_str = str( play_obj )
    # if not( match_obj.last_sign is None ):
    #     play_str = play_str + match_obj.last_sign
    
    # play_sign = request_msg[ "sign" ]
    # if not verify_signature( play_sign , play_str , pubk ):
    #     raise illegalMethod( "Play signature is not valid" )
    # match_obj.last_sign = play_sign

    plyr_1 = ( get_player_tag( match_id , player_id ) == PLAYER_1 )
    match_obj.push_move( play_obj , plyr_1 )

    response_dict = { "flag" : "ok" , "args" : {} } 
    return response_dict
    

def _check_mstate( request_msg ):
    
    player_id = request_msg["player_id"]
    player_data = get_player( player_id )
    match_id = player_data[ "current_match" ]
    if match_id is None:
        raise illegalMethod( "Player has no match" )
    
    match_obj : match_fsm = get_match_obj( match_id )
    if match_obj is None:
        raise illegalMethod( f"match {match_id} has not yet started" )

    tag = get_player_tag( match_id , player_id )
    response_msg = {
        "flag" : "ok",
        "args" : match_obj.to_dict( tag == PLAYER_1 )
    }

    return response_msg

method_dict = {
    "log_in" : _log_in,
    "log_out" : _log_out,
    "sample_players"  : _smp_players,
    "create_match" : _create_match,
    "join_match" : _join_match,
    "push_play" : _push_play,
    "check_mstate" : _check_mstate,
}


def get_request( sentence : bytes , addr : str ):
    
    try:
        str_payload = sentence.decode()
        json_payload : dict = loads( str_payload )
    except:
        raise invalidPayloadError("")

    # checking if it has necessary keys
    for kname in [ "method" , "args" ]:
        if not ( kname in json_payload.keys() ):
            raise invalidPayloadError( f"field {kname} not found in payload" )
    
    # checking if cmd exists
    requested_method = json_payload[ "method" ]
    if not ( requested_method in method_dict ):
        raise unknownMethod( f"method {requested_method} is a not known" )

    # finally returning the formatted method
    method_args = json_payload["args"]
    method_args[ "addr" ] = addr
    return requested_method , method_args

