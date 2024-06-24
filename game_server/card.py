
class card:

    Ranks = [ "CP" , "ES" , "OR" , "PA" ]
    Values = [ "A" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" , "10" ]

    def __init__( self , value : str , rank : str ):

        self.value = value
        self.rank  = rank
    
    def __str__( self ) -> str:
        return f"{self.value}-{self.rank}"
    
    def __eq__( self , other ) -> bool:
        return self.value == other.value and self.rank == other.rank
    
    def __gt__( self , other ) -> bool:
        
        '''
        self representa uma carta mais forte que other
        '''

        pos_1  = card.Values.index( self.value )
        rank_1 = card.Ranks.index( self.rank )

        pos_2  = card.Values.index( other.value )
        rank_2 = card.Ranks.index( other.rank )

        a = pos_1 > pos_2
        b = pos_1 == pos_2
        c = rank_1 > rank_2

        return a or ( b and c )
    
    def __lt__( self , other ) -> bool:
        return other > self