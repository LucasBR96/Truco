from os import environ
import logging
import requests
import json as js
from util import *

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)
# set_logger( logger )

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def notice_response( response_data ):
    pass

def report_error( err ):
    pass

def check_match_report( match_dict ):
    
    resp = match_dict
    flag = validate_minichain( match_dict[ "mv_hist" ] , logger )
    return flag , resp

method_dict = {
    "check_report": check_match_report
}

def handle_advance(data):

    sender = data[ "metadata" ][ "msg_sender"]
    logger.info( f"\Advance request from {sender}" )
    
    msg = js.loads( hex2str( data[ "payload" ] ) )
    method_name = msg[ "method" ]
    method_args = msg[ "args" ]
    logger.info( f"requested_method: {method_name}")

    method = method_dict[ method_name ]
    flag , resp = method( method_args )
    resp_form = str2hex( js.dumps( resp ) )

    status , target = "accept" , "notice"
    if not flag:
        status , target = "reject" , "report"
    
    response = requests.post( rollup_server + "/" + target, json={"payload": resp_form } )    
    logger.info( f"Received {target} status {response.status_code} body {response.content}")

    # if response.status_code == 400:
    #     requests.post( rollup_server + "/" + target, json={"payload": response.content} )
    #     status = "reject"

    return status


def handle_inspect(data):
        
    sender = data[ "metadata" ][ "msg_sender"]
    logger.info( f"\nInspect request from {sender}" )
    logger.info( f"Hi!")

    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

logger.info(f"")
logger.info(f"--------------------- Truco Chain ---------------------")
logger.info( f"" )
while True:
    logger.info("Sending finish")
    response : requests.Response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        # logger.info( rollup_request )
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
