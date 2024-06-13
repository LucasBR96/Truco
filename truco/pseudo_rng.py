import time as t

def make_seed( ):
    base = 2**24 - 1
    now = int( 100*t.time() )
    return now%base

class pseudo_rng:

    a = 17
    b = 97
    base = 2**24

    def __init__( self , seed : int ):

        self.seed = seed
        self.x = seed

    def __call__( self ) -> float:

        x = self.x
        self.x = ( self.a*x + self.b )%self.base

        return x/self.base

class pseudo_shuffler:

    def __init__( self , n : int , seed : int ):

        self.n = n
        self.seq = list( range( n ) )
        self.rng = pseudo_rng( seed )
    
    def __call__( self ):

        seq = self.seq
        for i in range( self.n ):
            j = int( self.n*self.rng() )
            seq[ i ] , seq[ j ] = seq[ j ] , seq[ i ]
        
        return seq.copy()
