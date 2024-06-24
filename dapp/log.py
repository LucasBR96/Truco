import logging
import traceback

def set_logger( logger : logging.Logger ):
    global _logger
    _logger = logger

def log_info( msg : str ):

    global _logger
    _logger.info( msg )

def print_logo():
    log_info(f"")
    log_info(f"--------------------- Truco Chain ---------------------")
    log_info( f"" )
