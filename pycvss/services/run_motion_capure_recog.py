import argparse
import os
import pycvss.ffmpeg.fdcm as fdcm
import pycvss.ssd.detect as detect
from pathlib import Path


###############################################################################
def get_args() -> dict:
    """[summary]

    Returns:
        dict -- [description]
    """
    parser = argparse.ArgumentParser(
        description='Single Shot MultiBox Detection"
        "Using motion capture filtering.')

    parser.add_argument('-p', '--pth', type=str, default=None,
                        help="The path to the .pth SSD training model file.")
    parser.add_argument('-i', '--input', type=str, default=None,
                        help="The path to the input file.")
    parser.add_argument(
        '-o', '--output', type=str, default=None,
        help="The path to the output directory that will be created.")

    return parser.parse_args()


###############################################################################


class MotionDetectionManager:
    """[summary]
    """
    def __init__(self, weights_file_: str):
        """[summary]

        Arguments:
            weights_file_ {str} -- [description]
        """
        _file = Path(input_)
        if _file.exists() and not _file.is_file():
            raise FileNotFoundError(f'Invalid file: {input_}')

        # Initial setup of the SSD and fdcm detector
        self._ssd = detect.initialize_ssd(weights_file_)
        self._base_transform = detect.get_base_transform(self.ssd)
        self._detector = fdcm.Fdcm()

        self._input_file = None
        self._output_dir = None

    @property
    def input_file(self) -> str:
        """[summary]

        Returns:
            [type] -- [description]
        """
        return self._input_file

    @input_file.setter
    def input_file(self, input_: str) -> None:
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
    def output_dir(self) -> str:
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_) -> None:
        self._output_dir = output_

    def detect(self):
        # Process input file and output a batch of files that contain motion
        self._detector.input_file = self._input_file
        self._detector.process()

        

