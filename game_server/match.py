# from game_server.pseudo_rng import *
# from game_server.play import *
# from game_server.card import *
# from game_server.player import *
# from game_server.deck import *
# from dapp.util import *

from game_server.match_fsm import *
import time as t
import pandas as pd

global nxt_match_id
nxt_match_id = 0

OUT = 0
PLAYER_1 = 1
PLAYER_2 = 2

OVER = "over"
WAITING = 'waiting'
PLAYING = 'playing'

def create_match_df( ):

    global match_df

    match_col = ["match_id" , "player_1_id" , "player_2_id" , "current_status" ]
    match_df : pd.DataFrame = pd.DataFrame( [] , columns = match_col )
    match_df.set_index( ["match_id"] , inplace = True )

    global match_objects
    match_objects = dict()

def match_exists( match_id ):
    global match_df
    return match_id in match_df.index

def get_player_tag( match_id , player_id ):
    global match_df

    if player_id == match_df.at[ match_id , "player_1_id" ]:
        return PLAYER_1
    
    if player_id == match_df.at[ match_id , "player_2_id" ]:
        return PLAYER_2
    
    return OUT

def player_in_match( match_id , player_id ):
    return get_player_tag( match_id , player_id ) != OUT

def add_match( player_id ):

    _id = nxt_match_id
    nxt_match_id += 1

    ser = pd.Series( 
        [ _id , player_id , None , WAITING ],
        index = ["match_id" , "player_1_id" , "player_2_id" , "current_status" ]
    )

    global match_df
    match_df.loc[ _id ] = ser

def join_match( match_id , player_id ):
    
    global match_df
    match_df.at[ match_id , "player_2_id" ] = player_id
    match_df.at[ match_id , "current_status" ] = PLAYING

    global match_objects
    match_objects[ match_id ] = match_fsm()
    

# class match:

#     _nxt_match_id = 0

#     def __init__( self , player_1 : player , player_2 : player = None ):

#         self._id = match._nxt_match_id
#         match._nxt_match_id += 1
#         self.start = t.time()
#         self._seed = make_seed()

#         # Player ip
#         self.player_1 = player_1 # Host
#         self.player_2 = player_2 # Visitor
#         self.fsm : match_fsm = match_fsm( self._seed , player_1 , player_2 )

#         # # Player public keys
#         # self.pubk = {
#         #     self.player_1 : pubk_1 ,
#         #     self.player_2 : pubk_2
#         # }

#         # # History of plays
#         # self.hist : play = []
#         # self.current_round : int = -1
#         # self.current_card_n : int = 0

#         # #Scoring
#         # self.match_score = {
#         #     self.player_1 : 0 , self.player_2 : 0
#         # }
#         # self.round_score = {
#         #     self.player_1 : 0 , self.player_2 : 0
#         # }

#         # # deck
#         # self._seed = make_seed()
#         # self.deck = deck( self._seed )

#         # # hands
#         # self.player_hands = {
#         #     self.player_1 : None , self.player_2 : None
#         # }
    
#     def add_player( self , plyr : player ):
#         self.player_2 = plyr
#         self.fsm.player_2 = plyr
#         self.fsm.state = match_fsm._x1
        
#         self.player_1.status = player.playing_status
#         self.player_2.status = player.playing_status
#         self.player_2.current_match = self._id


#     def player_in_game( self , player ):
#         return player == self.player_1 or player == self.player_2

#     def _switch_turn( self ):

#         a = self.player_turn == self.player_1
#         self.player_turn = self.player_2 if a else self.player_1
    
#     def _init_round( self ):

#         # setting the counter
#         self.current_round += 1
#         self.current_card_n = 0

#         # shuffling
#         self.deck.shuffle()

#         # dealing hands
#         player_hands = self.player_hands
#         player_hands[ self.player_1 ] = [ self.deck.deal_card() for _ in range( 3 ) ]
#         player_hands[ self.player_2 ] = [ self.deck.deal_card() for _ in range( 3 ) ]
        
#     def get_hand( self , player ):

#         if not self.player_in_game( player ):
#             return None
#             # TODO raise exception
        
#         hand = self.player_hands[ player ]
#         pub_key = self.pubk[ player ]

#         # return [ rsa_encrypt( str( card_i ) , pub_key ) for card_i in hand ]