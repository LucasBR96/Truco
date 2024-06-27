from card import *
from pseudo_rng import *

from itertools import product

class deck:

    card_l = list( product( card.Values , card.Ranks ) )

    def __init__( self , seed ):

        self._shuffler : pseudo_shuffler = pseudo_shuffler( 40 , seed )

        self.cards = None
        self.counter = None #cards remaining
        self.shuffle()
    
    def __getitem__( self , idx : int ) -> card:

        val , rank = self.cards[ idx ]
        return card( val , rank )

    def __call__( self ):

        '''
        removes top card and returns to the player
        '''

        top_card = self[ self.counter ]
        self.counter += 1
        return top_card
    
    def shuffle( self ):

        self.counter = 0

        seq = self._shuffler()
        self.cards = [ deck.card_l[ x ] for x in seq ]
