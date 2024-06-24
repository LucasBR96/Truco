class requestError( Exception ):

    def __init__( self , msg , err_type ):
        self.msg = msg
        self.type = err_type
        super().__init__( msg )

class invalidPayloadError( requestError ):

    def __init__( self , msg ):
        self.msg = msg
        super().__init__( msg , "invalid_payload")

class unknownMethod( requestError ):

    def __init__( self , msg ):
        self.msg = msg
        super().__init__( msg , "unknown_method")

class illegalMethod( requestError ):
    
    def __init__( self , msg ):
        self.msg = msg
        super().__init__( msg , "illegal_method" )