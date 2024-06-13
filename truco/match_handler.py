from truco.match import *
from truco.protocol import *
from truco.log import *

class match_handler:


    def __init__( self ):

        self.active_players : set = {}
        self.open_matches = dict()
        self.running_matches = dict()

        self.nxt_match_id = 0

        pass

    def handle_advance( self , command ):

        command_types = {
            "CG" : self._create_game( command )
        }
        cmd = command[ "cmd" ]
        fun = command_types[ cmd ]

        response = fun( command )
        log_info( f"{str(response)}")

        # try:
        #     response = fun( command )
        #     log_info( f"{str(response)}")

        # except Exception as ex:
        #     raise ex

        return response
    
    def handle_inspect( self , inspect_request ):
        pass

    def _create_game( self , command ):

        if command[ "player" ] in self.active_players:
            return
            # TODO Error handling
        
        # adding to active players
        self.active_players.add( command[ "player" ] )

        # creating match
        _id = self.nxt_match_id
        self.nxt_match_id += 1
        new_game = match( 
            _id,
            command["player_id"],
            command[ "pubk" ]
        )
        self.open_matches[ _id ] = new_game

        # generating response
        response = {
            "gid" : _id,
            "gseed" : new_game._seed,
            "gowner" : new_game.player_1
        }

        return response