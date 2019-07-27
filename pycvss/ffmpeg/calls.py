import pycvss.utils as utils


###############################################################################
# Decorator call functions

@utils.dec_exec_output_stream
def call_args(funct):
    """Call arguments from a given function

    Arguments:
        funct {function} -- Lambda containing stored function call

    Returns:
        List -- Function is expected to return a list of arguments
    """
    return funct()


@utils.dec_calculate_time
@utils.dec_exec_output_stream
def call_log_args(funct):
    """Call arguments from a given function and benchmark the call

    Arguments:
        funct {function} -- Lambda containing stored function call

    Returns:
        List -- Function is expected to return a list of arguments
    """
    return funct()
