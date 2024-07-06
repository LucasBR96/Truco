from socket import *
from json import dumps , loads
from util import *

from play import *

def log_in( player_id , pubk ):
    
    request = { "player_id" : player_id , "pubk" : pubk }
    flag , resp = send_request( "log_in" , request )
    if flag:
        return "OK"
    return resp
    # return flag , resp

def log_out( player_id ):

    request = { "player_id" : player_id }
    flag , resp = send_request( "log_out" , request )
    if flag:
        return "OK"
    return resp
    # return flag , resp

def create_match( player_id ):
    
    request = { "player_id" : player_id  }
    flag , resp = send_request( "create_match" , request )
    # if flag:
    #     match_id = resp["match_id"]
    #     return f"OK MATCH_ID {match_id}"
    # return resp
    return flag , resp 

def join_match( player_id , match_id ):

    request = { "player_id" : player_id , "match_id" : match_id }
    flag , resp = send_request( "join_match" , request )
    # if flag:
    #     return "OK"
    # return resp
    return flag , resp

def check_mstate( player_id ):

    request = { "player_id" : player_id  }
    flag , resp = send_request( "check_mstate" , request )
    if not flag:
        return resp
    
    match_dict = resp
    
    s = f"OK" + "\n"
    for k , v in match_dict.items():
        s += "\n" + f"{k} : {v}"
    return s
    # return flag , resp

def update_hist( player_id , mv_hist ):

    request = { "player_id" : player_id  }
    flag , resp = send_request( "check_mstate" , request )

    last_play , last_sign = resp[ "last_mv" ] , resp[ "last_sign"] 
    if last_play is None:
        return
    
    last_record = ''
    if len( mv_hist ) != 0:
        last_record = mv_hist[ -1 ][ 0 ]
    
    if last_record != last_play:
        mv_hist.append( ( last_play , last_sign ) )


def push_play( player_id , match_id , play_str , sign_str ):

    request = { 
        "player_id" : player_id,
        "match_id" : match_id,
        "play_str" : play_str,
        "sign_str" : sign_str
    }
    
    return send_request( "push_play" , request )


def send_request( request_type , request_args ):


    request_body = {
        "method" : request_type,
        "args"   : request_args
    }

    HOST = "127.0.0.1"
    PORT = 12000  # The port used by the server
    with socket(AF_INET, SOCK_STREAM) as s:

        s.connect((HOST, PORT))
        s.sendall( dumps( request_body ).encode() )
        data = loads( s.recv(2048) )
    
    flag = ( data[ "flag" ] == "ok" )
    if flag:
        resp = data["args"]
    else:
        err_type = data[ "err_type" ]
        msg = data[ "msg" ]
        resp = f"{err_type} : {msg}"
    return flag , resp


class fe_protocol:

    def __init__( self , player_id , pubk , pvtk ):
        
        self.player_id = player_id
        self.pubk = pubk
        self.pvtk = pvtk
    
        self.mv_hist = list()
        self.match_id = None
        self.match_state = None
    
    def log_in( self ):
        return log_in( self.player_id , self.pubk )
    
    def log_out( self ):
        return log_out( self.player_id )
    
    def create_match( self ):

        flag , resp = create_match( self.player_id )
        if flag:
            match_id = resp["match_id"]
            self.match_id = match_id

            return f"OK MATCH_ID {match_id}"
        return resp
    
    def join_match( self , match_id ):

        flag , resp = join_match( self.player_id , match_id )
        if flag:
            self.match_id = match_id
            return "OK"
        return resp
    
    def check_mstate( self ):
        
        request = { "player_id" : self.player_id  }
        flag , resp = send_request( "check_mstate" , request )

        self.match_state = resp

        last_play , last_sign = resp[ "last_mv" ] , resp[ "last_sign"] 
        if last_play is None:
            return
    
        last_record = ''
        if len( self.mv_hist ) != 0:
            last_record = self.mv_hist[ -1 ][ 0 ]
    
        if last_record != last_play:
            self.mv_hist.append( ( last_play , last_sign ) )

    def get_mstate( self ):

        s = f"OK" + "\n"
        for k , v in self.match_state.items():
            s += "\n" + f"{k} : {v}"
        print( s )

    def generate_play_str( self , card_val , card_rank ):

        n = len( self.mv_hist )
        round = n//6
        turn = ( n%6 )//2

        return str( play(
            self.match_id,
            round,
            turn,
            self.player_id,
            card_val,
            card_rank
        ) )
    
    def generate_sign_str( self , play_str ):

        last_sign = None
        if self.mv_hist:
            last_sign = self.mv_hist[ -1 ][ 1 ]
        
        return make_signature( play_str , last_sign )
    
    def push_play( self , card_val , card_rank ):

        play_str = self.generate_play_str( card_val , card_rank )

        update_hist( self.player_id , self.mv_hist )
        sign_str = self.generate_sign_str( play_str )

        flag , resp = push_play( self.player_id , self.match_id , play_str , sign_str )
        if flag:
            self.mv_hist.append( ( play_str , sign_str ) )
            return "OK"
        return resp
    
    def report_match( self ):
        
        match_report = dict()
        match_report[ "match_id" ] = self.match_id
        match_report[ "player_1" ] = self.match_state[ "player_1" ]
        match_report[ "player_2" ] = self.match_state[ "player_2" ]
        match_report[ "seed" ] = self.match_state[ "seed" ]
        match_report[ "winner" ] = self.match_state[ "winner" ]

        match_report[ "num_plays" ] = len( self.mv_hist )
        match_report[ "mv_hist" ] = self.mv_hist

        return match_report