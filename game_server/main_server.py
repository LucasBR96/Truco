import os
print( os.getcwd() )

from socket import *
from json import dumps , loads
from select import select
import logging

from protocol import get_request , method_dict
from errors import *

def fetch_connection( serverSocket : socket ):

    timeout = .1 
    ready_sockets, _, _ = select.select(
        [serverSocket], [], [], timeout
    )

    if not ready_sockets:
        return None
    return serverSocket.accept()

def handle_response( connection_socket : socket , response_data : dict ):
    response_str = dumps( response_data ).encode()
    connection_socket.send( response_str )


def handle_error( connection_socket: socket , err ):

    logger.error( f"{err.type} : {err.msg}")

    response = {
        "flag" : "not ok",
        'err_type' : err.type,
        "msg"  : err.msg
    }

    handle_response( connection_socket , response )


if __name__ == "__main__":

    logging.basicConfig(level="INFO")
    logger = logging.getLogger(__name__)

    logger.info( "truco backend is on line" )
    serverSocket = socket(AF_INET, SOCK_STREAM)

    server_host = "127.0.0.1"
    logger.info( f"current ip addr {server_host}" )

    serverPort = 12000
    logger.info( f"current port {serverPort}" )

    serverSocket.bind((server_host , serverPort ))
    serverSocket.listen(1)
    while True:

        # tup = fetch_connection( serverSocket )
        # if tup is None:
        #     continue
        
        tup = serverSocket.accept()
        connection_socket , ( addr , port ) = tup
        logger.info(f"")
        logger.info( f"connection from {addr}" )

        try:

            sentence = connection_socket.recv(1024)
            logger.info( f"raw payload: { sentence }")

            requested_method , request = get_request( sentence , addr )
            # logger.info( f"decoded payload: {request}")

            method = method_dict[ requested_method ]
            response_data = method( request )
            logger.info(f"response payload: {response_data}")
            handle_response( connection_socket , response_data  )

        except requestError as err:
            handle_error( connection_socket , err  )
    
        connection_socket.close()
        


            

            
    
