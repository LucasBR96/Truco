from os import environ
import logging
import requests
from truco.log import *
from truco.constantes import *
from truco.util import *
from truco.protocol import *
from truco.match_handler import *
from truco.errors import *

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)
# set_logger( logger )

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def notice_response( response_data ):
    pass

def report_error( err ):
    pass

def handle_advance(data):

    sender = data[ "metadata" ][ "msg_sender"]
    load = data[ "payload" ]
    logger.info( f"\nmessage from {sender}" )
    logger.info( f"raw payload {load}")

    try:
        command = get_command( sender , load )
        logger.info( f"decoded payload {command}" )

        requested_method = command["cmd"]
        method = advance_methods[ requested_method ]
        response_data = method( command )
        logger.info( f"response data {response_data}\n" )

        notice_response( response_data )
        return "accept"
    
    except Exception as err:

        if isinstance( err , requestError ):
            report_error( err )
        else:
            logger.error( f"{str(err)}")
        
        return "reject"

    # # checking if it is a json object -----------------------
    # command = get_command( load )
    # if command is None:
    #     log_info(f"unknown payload, message rejected\n")
    #     return "reject"
    # log_info( f"decoded payload {command}" )

    # # checking if it is in a valid format -------------------
    # if not check_command( command ):
    #     log_info(f"unknown command\n" )
    #     return "reject"
    
    # cmd = advance_methods[ command[ "cmd" ] ]
    # response_data = cmd( sender , command )
    # if response_data is None:
    #     log_info( f"illegal command\n" )
    #     return "reject"

    # log_info( f"response data {response_data}\n")
    # return "accept"


def handle_inspect(data):
    log_info(f"Received inspect request data {data}")
    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

print_logo()
while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
