from card import card

class play:

    def __init__( self , game_id : int , round_n : int , card_n : int , player_id : int , value , rank ):

        '''
        Cada jogada individual
        '''

        self.match_id = game_id
        self.round_n = round_n
        self.card_n = card_n
        self.player_id = player_id
        self.card_obj = card( value , rank )

    
    def __str__( self ):

        return str( self.match_id ) + "-" + \
        str( self.round_n ) + "-" + \
        str( self.card_n ) + "-" + \
        str( self.player_id ) + "-" + \
        str( self.card_obj )

