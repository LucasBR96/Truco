from truco.pseudo_rng import *
from truco.play import *
from truco.card import *
# from truco.message import *
from truco.deck import *
from truco.util import *

class match:

    def __init__( self , _id , player_1_address, pubk_1 , player_2_address = None , pubk_2 = None ):

        self._id = _id

        # Player ip
        self.player_1 = player_1_address # Host
        self.player_2 = player_2_address # Visitor
        self.player_turn = self.player_1

        # Player public keys
        self.pubk = {
            self.player_1 : pubk_1 ,
            self.player_1 : pubk_2
        }

        # History of plays
        self.hist : play = []
        self.current_round : int = -1
        self.current_card_n : int = 0

        #Scoring
        self.match_score = {
            self.player_1 : 0 , self.player_2 : 0
        }
        self.round_score = {
            self.player_1 : 0 , self.player_2 : 0
        }

        # deck
        self._seed = make_seed()
        self.deck = deck( self.seed )

        # hands
        self.player_hands = {
            self.player_1 : None , self.player_2 : None
        }

    def player_in_game( self , player ):
        return player == self.player_1 or player == self.player_2

    def _switch_turn( self ):

        a = self.player_turn == self.player_1
        self.player_turn = self.player_2 if a else self.player_1
    
    def _init_round( self ):

        # setting the counter
        self.current_round += 1
        self.current_card_n = 0

        # shuffling
        self.deck.shuffle()

        # dealing hands
        player_hands = self.player_hands
        player_hands[ self.player_1 ] = [ self.deck.deal_card() for _ in range( 3 ) ]
        player_hands[ self.player_2 ] = [ self.deck.deal_card() for _ in range( 3 ) ]
        
    def get_hand( self , player ):

        if not self.player_in_game( player ):
            return None
            # TODO raise exception
        
        hand = self.player_hands[ player ]
        pub_key = self.pubk[ player ]

        return [ rsa_encrypt( str( card_i ) , pub_key ) for card_i in hand ]