# from game_server.pseudo_rng import *
# from game_server.play import *
# from game_server.card import *
# from game_server.player import *
# from game_server.deck import *
# from dapp.util import *

from match_fsm import *
import time as t
import pandas as pd

nxt_match_id = 0

OUT = 0
PLAYER_1 = 1
PLAYER_2 = 2

OVER = "over"
WAITING = 'waiting'
PLAYING = 'playing'

match_df : pd.DataFrame

def create_match_df( ):

    global match_df

    match_col = ["match_id" , "player_1_id" , "player_2_id" , "current_status" ]
    match_df = pd.DataFrame( [] , columns = match_col )
    match_df.set_index( ["match_id"] , inplace = True )

    global match_objects
    match_objects = dict()

def match_exists( match_id ):
    global match_df
    return match_id in match_df.index

def get_match( match_id ):
    global match_df
    return match_df.loc[ match_id ]

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

    global nxt_match_id
    _id = nxt_match_id
    nxt_match_id += 1

    ser = pd.Series( 
        [ _id , player_id , None , WAITING ],
        index = ["match_id" , "player_1_id" , "player_2_id" , "current_status" ]
    )

    global match_df
    match_df.loc[ _id ] = ser

    return _id

def join_match( match_id , player_id ):
    
    global match_df
    match_df.at[ match_id , "player_2_id" ] = player_id
    match_df.at[ match_id , "current_status" ] = PLAYING

    global match_objects
    player_1 = match_df.at[ match_id , "player_1_id" ]
    match_objects[ match_id ] = match_fsm( player_1 , player_id )

def get_match_obj( match_id ):
    return match_objects.get( match_id , None )

