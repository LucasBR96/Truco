from truco.play import *
from truco.protocol import *
from truco.log import *

class player:

    # player status ---------------------------------
    idle_status = "idle"
    waiting_status = "waiting"
    playing_status = "playing"

    def __init__( self , _id , wallet_address , pub_k  ):

        self._id = _id
        self.wallet_address = wallet_address
        self.pub_k = pub_k
        
        self.status = player.idle_status
        self.current_match = None
    
    def __hash__( self ):
        return hash( self._id )
    
    def to_dict( self ):
        return self.__dict__()
    
    def sign_play( self , play_obj : play , last_sgn : str ) -> str:
        pass
