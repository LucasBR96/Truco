from os import environ
import logging
import requests
from truco.log import *
from truco.constantes import *
from truco.util import *
from truco.protocol import *
from truco.match_handler import *

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)
set_logger( logger )

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
log_info(f"HTTP rollup_server url is {rollup_server}")

m_handler = match_handler()
def handle_advance(data):

    md = data[ "metadata" ]
    load = data[ "payload" ]

    sender = md["msg_sender"]
    log_info(f"Received advance request from {hex2str(sender) }{ADDRESS_C} ")
    log_info(f"")

    try:
        status = "accept"
        target = "notice"
        command = get_command( md , load )

        response = m_handler.handle_advance( command )

    except Exception as ex:
        raise ex

    return status


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
