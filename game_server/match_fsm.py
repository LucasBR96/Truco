from game_server.play import *
from game_server.card import *
from game_server.deck import *
from game_server.pseudo_rng import *

WIN_1 = "w1"
WIN_2 = "w2"
A0 , A1 , A2 = "a0" , "a1" , "a2"
B0 , B1 , B2 = "b0" , "b1" , "b2" 

class match_fsm:
    
    '''
    match finite state machine.
    handles in match game logic.
    '''

    def __init__( self ):

        self.deck = deck( make_seed() )
        self.plyr_1_nxt = True
        self.turn = 0

        # self.curr_round = -1
        # self.hand_1 = None
        # self.hand_2 = None
        # self.table_1 = None
        # self.table_2 = None
        # self._init_round()

        self.score_1 = 0
        self.score_2 = 0

        # self.in_round_score_1 = 0
        # self.in_round_score_2 = 0
        
        pass

    def _init_round( self ):
        pass

    def get_state( self ):
        
        if self.score_1 == 12:
            return WIN_1
        
        if self.score_2 == 12:
            return WIN_2
        
        letter = "a" if self.plyr_1_nxt else "b"
        turn = str( self.turn )
        return letter + turn

    def push_move( self , move : play , plyr_1 = True ):

        answ , err = self._is_move_valid( move , plyr_1 )
        if not answ:
            raise err
        
        state = self.get_state()
        

    
    def _is_move_valid( self , move : play , plyr_tag ):

        pass