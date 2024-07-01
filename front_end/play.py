from card import card

class play:

    @classmethod
    def from_str( cls , str_arg : str ):

        str_vals = str_arg.split( "-" )
        return cls(
            int( str_vals[ 0 ] ), # match id
            int( str_vals[ 1 ] ), # round_n
            int( str_vals[ 2 ] ), # card_n
            str_vals[ 3 ],        # player_id
            str_vals[ 4 ],
            str_vals[ 5 ]
        )

    def __init__( self , game_id : int , round_n : int , card_n : int , player_id : str , value , rank ):

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
    



