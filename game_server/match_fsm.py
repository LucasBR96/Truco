from truco.play import *
from truco.card import *
from truco.player import *
from truco.deck import *

class match_fsm:
    
    '''
    match finite state machine.
    handles in match game logic.
    '''

    _x1 = "x1"
    _x2 = "x2"
    _12 = "12"
    _21 = "21"
    _win_1 = "win_1"
    _win_2 = "win_2"

    def __init__( self , seed ):

        self.deck = deck( seed )
        self.plyr_1_nxt = True
        self.turn = 0

        self.curr_round = -1
        self.hand_1 = None
        self.hand_2 = None
        self.table_1 = None
        self.table_2 = None
        self._init_round()

        self.score_1 = 0
        self.score_2 = 0

        self.in_round_score_1 = 0
        self.in_round_score_2 = 0
        
    def _init_round( self ):
        pass

    def _get_state( self ):
        pass 