import os
from pathlib import Path
import pycvss.ffmpeg.calls as calls
import pycvss.utils as utils


###############################################################################
def prepend_current_dir(file_: str) -> str:
    """Prepent the current working directory to a file

    Arguments:
        file_ {str} -- File to be prepented to

    Returns:
        str -- A string containing the new file path
    """
    return os.path.join(os.getcwd(), file_)


def handle_file_cleanup(file_: str):
    """Handles cleanup of a file

    Arguments:
        file_ {str} -- File to be cleaned up
    """
    try:
        output = Path(file_)
        os.remove(output)
    except FileNotFoundError:
        print(f"Skipping file: '{file_}': File not found.")


###############################################################################
class BTest:
    """Object that encapsulates a benchmark test, a benchmark test allows
    for an input function to be benchmarked.
    """
    def __init__(self, name_: str, args_func_,
                 input_file_: str=None, output_file_: str=None):
        """
        Arguments:
            name_ {str} -- Name of the function
            args_func_ {[type]} -- Function to test

        Keyword Arguments:
            input_file_ {str} -- Input file (default: {None})
            output_file_ {str} -- Output file (default: {None})
        """
        self._name = name_
        self._args_func = args_func_

        if input_file_ is None:
            self._input_file = None
        else:
            self.input_file = input_file_

        if output_file_ is None:
            self._output_file = None
        else:
            self.output_file = output_file_

    @property
    def input_file(self) ->str:
        return self._input_file

    @input_file.setter
    def input_file(self, input_: str):
        _file = Path(input_)
        if _file.exists() and not _file.is_file():
            raise FileNotFoundError(f'Invalid file: {input_}')

        name_parts = _file.name.split('.')
        if len(name_parts) == 2 and name_parts[1].upper() in utils.FILE_FORMATS:
            self._input_file = input_
        else:
            raise Exception('Invalid file format.')

    @property
    def output_file(self) -> str:
        return self._output_file

    @output_file.setter
    def output_file(self, output_: str) -> str:
        output_str_list = output_.split('.')
        if len(output_str_list) < 2:
            raise Exception('No file format specified')

        if output_str_list[1].upper() not in utils.FILE_FORMATS:
            raise Exception('Invalid file format.')

        self._output_file = output_

    def process(self) ->tuple:
        """Presses the test

        Raises:
            FileNotFoundError: If the input or output file
            do not exist

        Returns:
            tuple -- A tuple containing the name of the test and the result
            of the benchmark
        """
        if self._input_file is None:
            raise FileNotFoundError('Input file not found.')

        if self._output_file is None:
            raise FileNotFoundError('Output file not found.')

        with utils.TemporaryCopy(self._input_file) as input_copy:
            args = self._args_func()
            pos = 0
            # Find the input argument in the passed function, and replace it
            # with the temporary file
            for i, arg in enumerate(args):
                f = Path(arg)
                if f.exists() and f.is_file():
                    pos = i
                    break

            args[pos] = input_copy
            assert args[pos] == input_copy
            # call_log_args accepts a function so we'll wrap args in a lambda
            result = calls.call_log_args(lambda: args)

        # Clean up output file
        handle_file_cleanup(prepend_current_dir(self._output_file))

        return (self._name, result)
