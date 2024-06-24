# from game_server.match import *

import pandas as pd

from player import *
from errors import *
from match import *

from json import loads , dumps
import time as t
# ------------------------------------------------------------
# Jogos

# player_col = ["player_id" , "session_num" , "pubk" , "status" , "current_match" ]
# logged_players : pd.DataFrame = pd.DataFrame( [] , columns = player_col )
# logged_players.set_index( "player_id" )
logged_players = dict()

# match_col = [ "match_id" , "player_1", "player_2" , "status" ]
current_matches : dict = dict()

def _log_in( request_msg ):

    '''
    Player connects to the server

    Request:
        { "player_id" : <playerId> , "addr": <playerIp> , "pubk" : playerPubKey }
    response:
        { flag : "ok" , args : [ player_id , session_num , timestamp ] }
    '''

    player_id = request_msg[ "player_id"]
    if player_id in logged_players:
        raise illegalMethod( f"player {player_id} is already logged in" )
    
    # ---------------------------------
    # saving player
    addr = request_msg[ "addr" ]
    pubk = request_msg[ "pubk" ]
    player_obj = player(player_id, addr, pubk )
    logged_players[ player_id ] = player_obj
    
    # ----------------------------------
    # making response
    response_dict = {
        "flag": "ok",
        "args" : {
            "player_id" : player_id,
            "session_num" : player_obj.session_num,
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
    if player_id in logged_players:
        player_obj = logged_players.pop( player_id )
    else:
        raise illegalMethod( f"Player {player_id} already logged out.")
    
    response_dict = {
        "flag": "ok",
        "args" : {
            "player_id" : player_id,
            "session_num" : player_obj.session_num,
            "timestamp" : t.time()
        }
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
    if player_id in logged_players:
        player_obj : player = logged_players.pop( player_id )
    else:
        raise illegalMethod( f"Player {player_id} already logged out.")
    
    # player must be idle -----------------------------------
    if player_obj.status != player.idle_status:
        raise illegalMethod( f"Player {player_id} is already active.")
    
    new_match = match( player_obj )
    current_matches[ new_match._id ] = new_match
    player_obj.status = player.waiting_status

    # response
    response_payload = {
        "flag": "ok",
        "args" :{
            "match_owner" : player_id,
            "match_id"    : new_match._id,
            "match_start" : new_match.start
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

    # check if player 
    player_id = request_msg[ "player_id" ]
    if player_id not in logged_players:
        raise illegalMethod( f"player {player_id} is not logged in" )
    
    # checking match existence
    match_id = request_msg[ "game_id" ]
    if match_id not in current_matches:
        raise illegalMethod( f"match #{match_id} does not exist" )
    
    target_match : match = current_matches[ match_id ]
    a = target_match.player_1 is not None
    b = target_match.player_2 is not None
    if a and b:
        raise illegalMethod( f"match #{match_id} is full" )
    
    player_obj = logged_players[ player_id ]
    target_match.add_player( player_obj )
    # target_match.player_2 = logged_players[ player_id ]
    # target_match.player_2.status = player.playing_status
    # target_match.player_2.current_match = match_id

    # target_match.player_1.status = player.playing_status

    # making the response
    response : dict = {
        "flag" : "ok",
        "args" : {
            "match_id" : match_id,
            "timestamp" : t.time()
        }
    }
    return response

# def _check_matches( request_msg ):

#     '''
#     returns running games

#     request
#         { "player_id" : <playerId> , "addr" : PlayerAddr , "page_num" : num , "status" : "active" }
#     response
#         { "flag" : "ok" , "args" : { "list" : [ gamelist ] } }
#     '''
    
#     num = int( request_msg.get( "page_num") )


# def _push_play( request_msg ):
#     pass

# def _pinn_mstate( request_msg ):
#     pass

method_dict = {
    "log_in" : _log_in,
    "log_out" : _log_out,
    "create_match" : _create_match,
    # "check_games"  : _check_matches
    "join_match" : _join_match,
    "push_play" : _push_play,
    "ping_mstate" : _ping_mstate,
}


# Mensagens para Inspect state
# def _check_log( command ):

#     '''
#     allows player to check its own status in the server

#     request
#         { "cmd" : "check_log" , "player_id" : <PlayerId> , "args" : {} }
#     response
#         { "act" : "check_log" , "player_id" : <PlayerId> , "logged" : <Bool> , "player" : <playerObj> }
#     '''

#     player_id = command[ "player_id" ]
#     is_logged = ( player_id in logged_players )

#     response = { "act" : "check_log", "player_id" : player_id, "logged" : is_logged }
#     response[ "player_obj" ] = None
#     # if is_logged:
#     #     player_obj = logged_players[ player_id ]
#     #     response[ "player_obj" ] = player_obj.to_dict
    
#     return dumps( response )

# def _check_players( command ):
    
#     '''
#     allows player to check the logged players

#     request
#         { "cmd" : "check_players" , "player_id" : <PlayerId> , "args" : {} }
#     response
#         { "act" : "check_players" , "player_id" : <PlayerId> , "players" : [ <playerObj> ] }
#     '''

#     player_id = command[ "player_id" ]
#     response = { "act" : "check_players", "player_id" : player_id }
#     # response[ "players" ] = [
#     #     player_d.to_dict() for player_d in logged_players.values()
#     # ]

#     return dumps( response )

# def _check_games( command ):
#     pass



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

