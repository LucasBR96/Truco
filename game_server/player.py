import pandas as pd

IDLE = 'idle'
WAITING = 'waiting'
PLAYING = 'playing'

PAGE_SZ = 5

player_df : pd.DataFrame

def make_player_df():

    global player_df

    player_col = ["player_id" , "pubk" , "status" , "current_match" ]
    player_df = pd.DataFrame( [] , columns = player_col )
    player_df.set_index( ["player_id"] , inplace = True )


def is_logged( player_id ):

    global player_df
    return player_id in player_df.index

def add_player( player_id , pubk ):

    ser = pd.Series( 
        [ player_id , pubk , IDLE , None ],
        index = ["player_id" , "pubk" , "status" , "current_match"]
    )

    global player_df
    player_df.loc[ player_id ] = ser

def get_player( player_id ):
    global player_df
    return player_df.loc[ player_id ]

def rmv_player( player_id ):

    global player_df
    player_df.drop( player_id )

def set_match( player_id , match_id ):

    global player_df
    player_df.at[ player_id , "current_match" ] = match_id

def set_status( player_id , status ):

    global player_df
    player_df.at[ player_id , "status" ] = status

def sample_players( status_filter = None ) -> pd.DataFrame:
    
    global player_df

    # applaying status filter
    where = player_df.copy()
    if not ( status_filter is None ):
        where = player_df.loc[ player_df["status"] == status_filter ]
    
    return where

# class player:

#     # session id -----------------------------------
#     session = 0

#     # player status ---------------------------------
#     idle_status = "idle"
#     waiting_status = "waiting"
#     playing_status = "playing"

#     def __init__( self , _id , wallet_address , pub_k  ):

#         self._id = _id
#         self.wallet_address = wallet_address
#         self.pub_k = pub_k
        
#         self.status = player.idle_status
#         self.current_match = None

#         self.session_num = player.session
#         player.session += 1 
    
#     def __hash__( self ):
#         return hash( self._id )
    
#     def to_dict( self ):
#         return self.__dict__()

