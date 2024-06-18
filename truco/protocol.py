from truco.util import *
from truco.log import *
from truco.match import *
from truco.player import *
from truco.errors import *


from json import loads , dumps
import time as t
# ------------------------------------------------------------
# Jogos

logged_players : dict = dict()
open_matches : dict = dict()
current_matches : dict = dict()

def _create_game( command ):

    ''' 
    1) Create Game
    request:
        { "cmd" : "create_game" , "player_id" : <playerId> , "args" : {} }
    response:
        { "game_id" : <gameId> , "game_seed" : <gameSeed> , "game_owner" : <OwnerId> }
    '''

    # checking legallity ---------------------------------
    player_id = command[ "player_id"]
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
        "act": "create_game",
        "player_id" : player_id,
        "match_id": new_match._id,
        "match_seed" : new_match._seed,
        "match_start" : new_match.start
    }

    return dumps( response_payload )

def _join_game( command ):

    '''
    player joins a running game

    Request:
        { "cmd" : "join_game" , "player_id" : <playerId> , "args" : { "game_id" : <id> } }
    response:
        { "act" : "join_game" , "player_id": <playerId>, "match_id" : match_id, "timestamp" : <logTime> }
    '''

    # check if player 
    player_id = command[ "player_id"]
    if player_id not in logged_players:
        raise illegalMethod( f"player {player_id} is not logged in" )
    
    # checking match existence
    match_id = command["args"][ "game_id" ]
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
        "act" : "join_game",
        "player_id" : player_id,
        "match_id" : match_id,
        "timestamp" : t.time()
    }
    return dumps( response )


def _validate_game( command ):
    pass

def _push_play( command ):
    pass

def _log_in( request_msg ):

    '''
    Player connects to the server

    Request:
        { "cmd" : "log_in" , "player_id" : <playerId> , "args" : { "pubk" : playerPubKey} }
    response:
        { "act" : ok , "player_id": <playerId>, "wallet" : <Wallet>, "pubk" : playerKey , "timestamp" : <logTime> }
    '''

    player_id = request_msg[ "player_id"]
    if player_id in logged_players:
        raise illegalMethod( f"player {player_id} is already logged in" )
    
    # ---------------------------------
    # saving player
    wallet = request_msg[ "wallet" ]
    pubk = request_msg[ "args" ][ "pubk" ]
    player_obj = player(player_id, wallet, pubk )
    logged_players[ player_id ] = player_obj
    
    # ----------------------------------
    # making response
    response_dict = {
        "act": "log_in",
        "player_id" : player_id,
        "wallet" : wallet,
        "pubk" : pubk,
        "timestamp" : t.time()
    }

    return dumps( response_dict )

def _log_out( request_msg ):

    '''
    Removes player from the server

    request:
        { "cmd" : "log_in" , "player_id" : <playerId> , "args" : {} }
    response:

    '''

    # checking legallity ---------------------------------
    player_id = request_msg[ "player_id"]
    if player_id in logged_players:
        player_obj = logged_players.pop( player_id )
    else:
        raise illegalMethod( f"Player {player_id} already logged out.")
    
    response_dict = {
        "act": "log_out",
        "player_id" : player_obj._id,
        "wallet" : player_obj.wallet_address,
        "timestamp" : t.time()
    }

    return dumps( response_dict )

advance_methods = {
    "log_in" : _log_in,
    "log_out" : _log_out,
    "create_game" : _create_game,
    "join_game" : _join_game,
    "validate_game" : _validate_game,
    "push_play" : _push_play
}


# Mensagens para Inspect state
def _check_log( command ):

    '''
    allows player to check its own status in the server

    request
        { "cmd" : "check_log" , "player_id" : <PlayerId> , "args" : {} }
    response
        { "act" : "check_log" , "player_id" : <PlayerId> , "logged" : <Bool> , "player" : <playerObj> }
    '''

    player_id = command[ "player_id" ]
    is_logged = ( player_id in logged_players )

    response = { "act" : "check_log", "player_id" : player_id, "logged" : is_logged }
    response[ "player_obj" ] = None
    # if is_logged:
    #     player_obj = logged_players[ player_id ]
    #     response[ "player_obj" ] = player_obj.to_dict
    
    return dumps( response )

def _check_players( command ):
    
    '''
    allows player to check the logged players

    request
        { "cmd" : "check_players" , "player_id" : <PlayerId> , "args" : {} }
    response
        { "act" : "check_players" , "player_id" : <PlayerId> , "players" : [ <playerObj> ] }
    '''

    player_id = command[ "player_id" ]
    response = { "act" : "check_players", "player_id" : player_id }
    # response[ "players" ] = [
    #     player_d.to_dict() for player_d in logged_players.values()
    # ]

    return dumps( response )

def _check_games( command ):
    pass

def _pinn_status( command ):
    pass

inspect_methods = {
    "check_players" : _check_players,
    "check_log" : _check_log,
    "pinn_status": _pinn_status,
    "check_games" : _check_games
}

def get_command( sender , payload , rqs_type = "advance"):
    
    try:
        str_payload = hex2str(payload)
        json_payload : dict = loads( str_payload )
    except:
        raise invalidPayloadError("")

    # checking if it has necessary keys
    for kname in [ "player_id" , "cmd" , "args" ]:
        if not ( kname in json_payload.keys() ):
            raise invalidPayloadError( f"field {kname} not found in payload" )
    
    # checking if cmd exists
    cmd_dict = advance_methods
    if rqs_type == "inspect":
        cmd_dict = inspect_methods
    method = json_payload.get( "cmd" , None )
    if not ( method in cmd_dict ):
        raise unknownMethod( f"method {method} is a not known {rqs_type} method" )

    # finally returning the formatted method
    json_payload[ "wallet" ] = sender
    return json_payload

