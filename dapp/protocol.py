# import pandas as pd
from util import *

match_reports = set()
player_dict = dict()

def check_match_report( match_dict ):
    
    mv_hist = match_dict[ "mv_hist" ]

    player_1 = match_dict[ "player_1" ]
    pubk_1 = player_dict[ player_1 ]

    player_2 = match_dict[ "player_2" ]
    pubk_2 = player_dict[ player_2 ]

    last_sign , flag = '' , True
    for play_str , sgn_str in mv_hist:

        player = play_str.split( sep = "-" )[ 3 ]
        pubk = pubk_1
        if player == player_2:
            pubk = pubk_2
        
        h_str = play_str + last_sign
        flag = verify_signature( h_str , sgn_str , pubk )

        if not flag:
            break

        last_sign = sgn_str
    
    if flag:
        resp = match_dict
        tup = (
            match_dict[ "reporter" ],
            match_dict[ "match_id" ]
        )
        match_reports.add( tup )
    else:
        resp = None
    
    return resp , flag


def log_in( log_in_dict ):

    player_id = log_in_dict[ "player_id" ]
    pubk = log_in_dict[ "pubk" ]

    player_dict[ player_id ] = pubk
    return True , log_in_dict

advance_methods = {
    "check_report": check_match_report,
    "log_in" : log_in
}

def confirm_mreport( player_id , match_id ):
    
    return str( ( player_id , int( match_id ) ) in match_reports )

def confirm_log_in( player_id ):
    return str( player_id in player_dict )


inspect_methods = {
    "confirm_report" : confirm_mreport,
    "confirm_log_in" : confirm_log_in
}