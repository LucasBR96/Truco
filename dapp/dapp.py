from os import environ
import logging
import requests

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
    logger.info( f"\Advance request from {sender}" )
    logger.info( f"Hi!")

    return "accept"


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
        logger.info( rollup_request )
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
