import os
from pathlib import Path
import pycvss.ffmpeg.calls as calls
import pycvss.utils as utils


######################################################################################
def prepend_current_dir(output_file_: str) -> str:
    """[summary]

    Arguments:
        output_file_ {str} -- [description]

    Returns:
        str -- [description]
    """
    return os.path.join (os.getcwd(), output_file_)


def handle_test_cleanup(output_file_: str) -> bool:
    """[summary]

    Arguments:
        output_file_ {str} -- [description]

    Returns:
        bool -- [description]
    """
    try:
        output = Path(output_file_)
        os.remove(output)
    except FileNotFoundError:
        print(f"Skipping file: '{output_file_}': File not found.")


######################################################################################
class BTest:
    """[summary]
    """
    def __init__(self, name_: str, args_func_, input_file_: str=None, output_file_: str=None):
        """[summary]

        Arguments:
            name_ {str} -- [description]
            args_func_ {[type]} -- [description]

        Keyword Arguments:
            input_file_ {str} -- [description] (default: {None})
            output_file_ {str} -- [description] (default: {None})
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
        """[summary]

        Returns:
            str -- [description]
        """
        return self._input_file

    @input_file.setter
    def input_file(self, input_: str) -> str:
        """[summary]

        Arguments:
            input_ {str} -- [description]

        Raises:
            FileNotFoundError: [description]
            Exception: [description]

        Returns:
            str -- [description]
        """
        _file = Path(input_)
        if _file.exists() and not _file.is_file():
            raise FileNotFoundError(f'Invalid file: {input_}')

        name_parts = _file.name.split('.')
        if len(name_parts) == 2 and name_parts[1] in utils.FILE_FORMATS:
            self._input_file = input_
        else:
            raise Exception('Invalid file format.')

    @property
    def output_file(self) -> str:
        """[summary]

        Returns:
            str -- [description]
        """
        return self._output_file

    @output_file.setter
    def output_file(self, output_:str ) -> str:
        """[summary]

        Arguments:
            output_ {str} -- [description]

        Raises:
            Exception: [description]
            Exception: [description]

        Returns:
            str -- [description]
        """
        output_str_list = output_.split('.')
        if len(output_str_list) < 2:
            raise Exception('No file format specified')

        if output_str_list[1] not in utils.FILE_FORMATS:
            raise Exception('Invalid file format.')

        self._output_file = output_

    def process(self) ->tuple:
        """[summary]

        Raises:
            FileNotFoundError: [description]
            FileNotFoundError: [description]

        Returns:
            tuple -- [description]
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
            assert(args[pos] == input_copy)
            # call_log_args accepts a function so we'll wrap args in a lambda
            result = calls.call_log_args(lambda: args)

        # Clean up output file
        handle_test_cleanup(prepend_current_dir(self._output_file))

        return (self._name, result)
