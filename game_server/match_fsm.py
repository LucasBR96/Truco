from play import *
from card import *
from deck import *
from pseudo_rng import *
from constantes import PLAYER_1 , PLAYER_2 , OUT
from errors import illegalMethod
        

class match_fsm:
    
    '''
    match finite state machine.
    handles in match game logic.
    '''

    def __init__( self ):

        self.deck = deck( make_seed() )
        self.plyr_1_nxt = True
        self.last_mv = None
        self.last_sign = None

        self.curr_round = -1
        self.turn = 0
        self.hand_1 = None
        self.hand_2 = None
        self.table_1 = None
        self.table_2 = None
        self.in_round_score_1 = 0
        self.in_round_score_2 = 0
        self._init_round()

        self.score_1 = 0
        self.score_2 = 0

        self.ack_1 = False
        self.ack_2 = False
        pass

    def _init_round( self ):
        
        self.deck.shuffle()
        self.hand_1 = [ self.deck() for _ in range( 3 ) ]
        self.hand_2 = [ self.deck() for _ in range( 3 ) ]
        self.table_1 = [ None , None , None ]
        self.table_2 = [ None , None , None ]
        
        self.curr_round += 1
        self.turn = 0
        self.in_round_score_1 = 0
        self.in_round_score_2 = 0

    def freeze( self ):

        self.ack_1 = False
        self.ack_2 = False
    
    def is_frozen( self ):

        ack = self.ack_1 and self.ack_2
        return not ack
    
    def _ack_state( self , plyr_1 : bool ):

        if plyr_1: 
            self.ack_1 = True
        else:
            self.ack_2 = True
    
    def ack_state( self , plyr_1 ):

        self._ack_state( plyr_1 )
        if self.is_frozen() : return
        if self.turn != 3 : return
        self._init_round()

    def get_winner( self ):
        
        if self.score_1 == 12:
            return PLAYER_1
        
        if self.score_2 == 12:
            return PLAYER_2
        
        return OUT

    def push_play( self , move : play , sgn_str , plyr_1 = True ):

        flag , msg = self._is_move_valid( move , plyr_1 )
        if not flag:
            raise illegalMethod( msg )
        self._push_move( move , sgn_str , plyr_1 )
        self._update_state()
        self.freeze()

    def _push_move( self , move : play , sgn_str ,plyr_1 = True ):

        self.last_mv = str( move )
        self.last_sign = sgn_str
        
        plr_table = self.table_1 if plyr_1 else self.table_2
        plr_card = move.card_obj
        plr_table[ self.turn ] = plr_card

        plr_hand : list = self.hand_1 if plyr_1 else self.hand_2
        plr_hand.remove( plr_card )

    
    def _is_move_valid( self , move : play , plyr_1 : bool ):

        if self.is_frozen():
            err_msg = f"The current match state must be seen by all players"
            return False , err_msg

        # ---------------------------------------------------
        # checking end of match
        win = self.get_winner()
        if win != OUT:
            err_msg = f"Match is over, player {win} has won."
            return False , err_msg

        # ---------------------------------------------------
        # checking if out of turn
        tag = PLAYER_1 if plyr_1 else PLAYER_2
        if plyr_1 != self.plyr_1_nxt:
            err_msg = f"Out of order. it is not player_{tag}'s turn."
            return False , err_msg
        
        # ---------------------------------------------------
        # checking correct hand
        plr_hand : list = self.hand_1 if plyr_1 else self.hand_2
        if move.card_obj not in plr_hand:
            err_msg = f"Card {move.card_obj} is not in player_{tag}'s hand."
            return False , err_msg
        
        # ------------------------------------------------------
        # checking correct cypher
        # TODO

        return True , ''

    

    def _update_state( self ):

        card_1 = self.table_1[ self.turn ]
        card_2 = self.table_2[ self.turn ]
        
        a = ( card_1 is None )
        b = ( card_2 is None )
        if a and b:
            return
        
        if ( card_1 is None ) or ( card_2 is None ):
            self.plyr_1_nxt = not self.plyr_1_nxt
            return 

        card_1 > card_2
        if card_1 > card_2:
            self.plyr_1_nxt = True
            self.in_round_score_1 += 1
        else:
            self.plyr_1_nxt = False
            self.in_round_score_2 += 1

        self.turn += 1
        if self.turn != 3:
            return
        
        if self.in_round_score_1 > self.in_round_score_2:
            self.score_1 += 1
        else:
            self.score_2 += 1
        
    
    def to_dict( self , plyr_1 : bool ):

        r_dict = {}
        
        r_dict[ "your_turn" ] = ( plyr_1 == self.plyr_1_nxt )
        r_dict[ "last_mv" ] = self.last_mv
        r_dict[ "last_sign" ] = self.last_sign
        r_dict[ "curr_round" ] = self.curr_round
        r_dict[ "turn" ] = self.turn
        r_dict[ "table_1" ] = [ str( c ) for c in self.table_1 ]
        r_dict[ "table_2" ] = [ str( c ) for c in self.table_2 ]
        r_dict[ "in_round_score_1" ] = self.in_round_score_1
        r_dict[ "in_round_score_2" ] = self.in_round_score_2

        hand =  self.hand_1
        if not plyr_1:
            hand = self.hand_2
        r_dict[ "hand" ] = [ str( c ) for c in hand ]

        r_dict[ "score_1" ] = self.score_1
        r_dict[ "score_2" ] = self.score_2

        return r_dict