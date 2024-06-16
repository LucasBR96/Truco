from truco.util import *
from truco.log import *
from truco.match import *
from truco.errors import *


from json import loads , dumps
import time as t
# ------------------------------------------------------------
# Jogos

logged_players : dict = dict()
active_players : set = set()
open_matches : dict = dict()
running_matches : dict = dict()

# '''

# Mensagens para advance state

# 2) Join Game
# request:
#     { "cmd" : "join_game" , "player_id" : <playerId> , "args" : { "pubk" : <playerPubKey>  ,  } }
# response:
#     { "game_id" : <gameId> , "game_seed" : <gameSeed> , "game_owner" : <OwnerId> }

# 3) Send Card
# 4) Validate Game
# 

# 1) Create Game
# request:
#     { "cmd" : "create_game" , "player_id" : <playerId> , "args" : {} }
# response:
#     { "game_id" : <gameId> , "game_seed" : <gameSeed> , "game_owner" : <OwnerId> }

def _create_game( sender : str , command ):
    
    if command[ "player_id" ] not in logged_players:
        return None
    
    if command[ "player_id" ] in active_players:
        return None

    
    _id = match._nxt_match_id
    match._nxt_match_id += 1

    new_match = match(
        _id,
        command[ "player_id"],
        logged_players[ command["player_id"] ][ "pubk" ]
    )
    open_matches[ _id ] = new_match

    active_players.add( command [ "player_id" ] )

    # response
    response_payload = {
        "id": _id,
        "game_seed" : new_match._seed,
        "game_owner" : command [ "player_id" ]
    }
    return dumps( response_payload )

# 5 ) Log In
# request:
#     { "cmd" : "log_in" , "player_id" : <playerId> , "args" : { "pubk" : playerPubKey} }
# response:
#     { "log_ok" : ok , "timestamp" : <logTime> }
#   
def _log_in( request_msg ):

    player_id = request_msg[ "player_id"]
    if player_id in logged_players:
        raise illegalMethod( f"player {player_id} is already logged in" )
    
    # ---------------------------------
    # saving player
    wallet = request_msg[ "wallet_id" ]
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

# 6 ) Log out 
def _log_out( request_msg ):

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
    "log_out" : _log_out
}


# Mensagens para Inspect state

# 1) Check Hand
# 2) Check Table
# 3) Check games

# 4) Check players
def _check_players( sender , command ):

    if command[ "player_id" ] in logged_players:
        return None


inspect_methods = {
    "check_players" : _check_players
}

def get_command( sender , payload , rqs_type = "advance"):
    
    try:
        str_payload = hex2str(payload)
        json_payload : dict = loads( str_payload )
    except:
        raise invalidPayloadError("")

    # checking if it has necessary keys
    for kname in [ "player_id " , "cmd" , "args" ]:
        if not ( kname in json_payload.values() ):
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


def check_command( json_payload , rqs_type = "advance" ) -> bool:

    cmd_dict = advance_methods
    if rqs_type == "inspect":
        cmd_dict = inspect_methods
    
    return json_payload.get( "cmd" , None ) in cmd_dict 
