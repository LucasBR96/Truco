'''

Mensagens para advance state

1) Create Game
request:
    { "cmd" : "CG" , "player_id" : <playerId> , "pubk" : <playerPubKey> }
response:
    { "gid" : <gameId> , "gseed" : <gameSeed> , "gameOwner" : <OwnerId> }

2) Join Game
request:
response:

3) Send Card
4) Validade Game


Mensagens para Inspect state

1) Check Hand
2) Check Table
3) Check games

'''
from truco.util import *
from truco.log import *

from json import loads

def get_command( meta_data , payload ):
    
    str_payload = hex2str(payload)
    log_info( f"decoded payload {str_payload} ")
    json_payload = loads( str_payload )

    # cmd_type = _check_command( json_payload )

    # if cmd_type is None:
    #     pass
        # raise Exception

    return json_payload

def _check_command( json_payload ):
    pass
