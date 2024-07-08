# import pandas as pd
from util import *

match_reports = set()

def check_match_report( match_dict ):
    
    resp = match_dict
    flag = validate_minichain( match_dict[ "mv_hist" ] )
    if flag:
        tup = (
            match_dict[ "reporter" ],
            match_dict[ "match_id" ]
        )
        match_reports.add( tup )
    return flag , resp

advance_methods = {
    "check_report": check_match_report
}

def confirm_mreport( player_id , match_id ):
    
    return str( ( player_id , match_id ) in match_reports )
 

inspect_methods = {
    "confirm_report" : confirm_mreport
}