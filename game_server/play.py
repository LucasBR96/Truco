from card import card
from hashlib import sha224

class play:

    def __init__( self , game_id : int , round_n : int , card_n : int , player_id : int , card : card ):

        '''
        Cada jogada individual
        '''

        self.game_id = game_id
        self.round_n = round_n
        self.card_n = card_n
        self.player_id = player_id
        self.card = card

        self.signature = None
    
    def __str__( self ):

        return str( self.game_id ) + "-" + \
        str( self.round_n ) + "-" + \
        str( self.card_n ) + "-" + \
        str( self.player_id ) + "-" + \
        str( self.card )

    def __hash__( self ):
        return sha224( str( self ).encode() ).hexdigest()