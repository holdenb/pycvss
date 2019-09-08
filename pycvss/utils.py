import os
import shutil
import tempfile
import subprocess
import time


# File formats
FILE_FORMATS = [
    'MP4', 'mp4', 'M4P', 'M4B', 'M4R', 'M4V',
    'M4A', 'DIVX', 'EVO', 'F4V', 'FLV',
    'AVI', 'QT', 'MXF', 'MOV', 'mov', 'MTS',
    'M2TS', 'MPEG', 'VOB', 'IFO']


######################################################################################
# Utility classes
class TemporaryCopy():
    """This object encapsulates the creation of a temporary
    copy of a file. This object is used as a context.
    """
    def __init__(self, original_path_: str):
        self._original_path = original_path_
        self._path = None

    def __enter__(self):
        temp_dir = tempfile.gettempdir()
        base_path = os.path.basename(self._original_path)
        self._path = os.path.join(temp_dir, base_path)
        shutil.copy2(self._original_path, self._path)

        return self._path

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self._path)


######################################################################################
# Utility functions

def get_current_path() -> str:
    """Gets the path of the current file being executed

    Returns:
        str -- A string containing the filepath
    """
    curr_path_including_file = os.path.realpath(__file__)
    path_list = curr_path_including_file.split('/')
    path_list.pop()
    return '/'.join(path_list)


def dec_calculate_time(func_):
    """Decorator for benchmarking a single function call

    example call:
    @dec_calculate_time
    def my_funct():
            pass

    Arguments:
    func {function} -- Function to benchmark

    Returns:
    function -- The decorated function
    """
    def decorated(*args, **kwargs):
        """Inner function to be decorated"""
        begin = time.time()
        func_(*args, **kwargs)
        end = time.time()

        return end - begin

    return decorated


def dec_exec_output_stream(func_):
    """Decorator for executing a subprocess argument list
    returned from a given decorated function. This decorator
    will also print stdout to the console.

    example call:
    @dec_exec_output_stream
    def my_funct():
            return args

    Arguments:
    func {function} -- Function that returns arguments
            that we should execute and then print process
            stdout

    Returns:
    function -- The decorated function
    """
    def decorated(*args, **kwargs):
        """Inner function to be decorated"""
        args_base = func_(*args, **kwargs)
        for path in execute(args_base):
            print(path, end="")

    return decorated


def execute(cmd_: list) -> None:
    """Executes a subprocess command

    Arguments:
    cmd {list} -- List of arguments to forward to the process

    Raises:
    subprocess.CalledProcessError
    """
    popen = subprocess.Popen(cmd_, stdout=subprocess.PIPE, universal_newlines=True)

    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line

    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd_)
