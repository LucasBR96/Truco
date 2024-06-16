class requestError( Exception ):

    def __init__( self , msg ):
        self.msg = msg
        super().__init__( msg )

class invalidPayloadError( requestError ):

    def __init__( self , msg ):
        self.msg = msg
        super().__init__( msg )

class unknownMethod( requestError ):

    def __init__( self , msg ):
        self.msg = msg
        super().__init__( msg )

class illegalMethod( requestError ):
    
    def __init__( self , msg ):
        self.msg = msg
        super().__init__( msg )