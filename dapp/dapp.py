from os import environ
import logging
import requests
import json as js
from util import *
from protocol import *

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)
# set_logger( logger )

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

# def notice_response( response_data ):
#     pass

# def report_error( err ):
#     pass

def handle_advance(data):

    sender = data[ "metadata" ][ "msg_sender"]
    logger.info( f"\Advance request from {sender}" )
    
    msg = js.loads( hex2str( data[ "payload" ] ) )
    method_name = msg[ "method" ]
    method_args = msg[ "args" ]
    logger.info( f"requested_method: {method_name}")

    method = advance_methods[ method_name ]
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


def handle_inspect( data : str ):

    decoded_payload = hex2str( data["payload"] ).decode() 
       
    query = decoded_payload.split( sep = "-" )
    method = inspect_methods[ query[ 0 ] ]
    resp = method( *query[1:] )

    resp_form = str2hex( resp )
    response = requests.post( rollup_server + "/report" , json={"payload": resp_form } )    
    logger.info( f"Received report status {response.status_code} body {response.content}")

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
        logger.info( rollup_request )
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
