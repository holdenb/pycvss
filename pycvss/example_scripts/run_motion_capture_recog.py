import argparse
import os
import imageio
import sys
import pycvss.sample_files as sample_files
import pycvss.utils as utils
import pycvss.ffmpeg.fdcm as fdcm
import pycvss.ssd.detect as detect
from pathlib import Path


###############################################################################
def get_args() -> dict:
    """Get arguments from the parser

    Returns:
        dict -- A dictionary of arguments
    """
    parser = argparse.ArgumentParser(
        description='Single Shot MultiBox Detection using motion'
        ' capture filtering.')

    parser.add_help

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
    """Manages FDCM and SSD modules. This object will process a video
    into segments, and then apply object classification to each frame in each
    segmented video.
    """
    def __init__(self, weights_file_: str):
        """
        Arguments:
            weights_file_ {str} -- SSD weights file
        """
        # Initial setup of the SSD and fdcm detector
        # SSD neural network
        self._ssd = detect.initialize_ssd(weights_file_)
        # SSD base transform tensor
        self._base_transform = detect.get_base_transform(self._ssd)
        # FDCM Detector
        self._detector = fdcm.Fdcm()
        # Input file
        self._input_file = None
        # Output directory
        self._output_dir = None

    @property
    def input_file(self) -> str:
        return self._input_file

    @input_file.setter
    def input_file(self, input_: str) -> None:
        _file = Path(input_)
        if _file.exists() and not _file.is_file():
            raise FileNotFoundError(f'Invalid file: {input_}')

        name_parts = _file.name.split('.')
        if len(name_parts) == 2 and \
           name_parts[1].upper() in utils.FILE_FORMATS:
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
        """Run detection on the input file

        Raises:
            Exception: If the input file or output directory
            do not exist
        """
        if self._input_file is None or self._output_dir is None:
            raise Exception(
                'Must specify an input file and output directory'
                'before running detection.')

        # Process input file and output a batch of files that contain motion
        self._detector.input_file = self._input_file
        self._detector._output_dir = self._output_dir
        self._detector.process()

        def run_ssd_detection(path_: str, name_: str) -> None:
            (frame_reader, fps) = detect.get_reader_fps_pair_from_stream(
                path_)

            # Build the new output file name
            (file_name, file_extension) = os.path.splitext(name_)
            output_filename = file_name + '_detected' + file_extension
            output_filename = self._output_dir + '/' + output_filename

            # Open the context and write to the new output file
            with imageio.get_writer(output_filename, fps=fps) as frame_writer:
                for i, frame in enumerate(frame_reader):
                    # Run detection on the frame
                    detected_frame = detect.detect_frame(
                        frame, self._ssd.eval(), self._base_transform)

                    # Append our detected frame to the video writer
                    frame_writer.append_data(detected_frame)
                    print(f'File: {file_name}: Processing frame: {i}')

        # Iterate through the directory contents and run frame by frame object
        # detection using our SSD
        target_file_extension = self._detector.output_file_extension()
        for filename in os.listdir(self._output_dir):
            if filename.endswith(target_file_extension):
                #TODO multi-thread this using the multiprocess module
                run_ssd_detection(self._output_dir + '/' + filename, filename)
                # Clean up old file after we're finished
                # os.remove(os.path.join(self._output_dir, filename))
            else:
                continue


###############################################################################
if __name__ == "__main__":
    args = get_args()
    pth_file = args.pth
    if pth_file is None:
        raise FileNotFoundError(
            "A .pth training file is required to run the SSD.")

    # NOTE For now, we'll use an sample file as backup
    # TODO Remove the sample file and throw if the user does not
    # specify an input file
    input_file = args.input
    if input_file is None:
        input_file = sample_files.SAMPLE_VIDEO_HD_MOV

    output_dir = args.output
    if output_dir is None:
        output_dir = os.path.dirname(sys.argv[0]) + os.sep + 'output_dir'

    manager = MotionDetectionManager(pth_file)
    manager.input_file = input_file
    manager.output_dir = output_dir
    manager.detect()
