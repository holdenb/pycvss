import os
import sys
from pathlib import Path

import ffmpeg_py.utils as utils

# FFMPEG input process base arguments
FFMPEG_INPUT_PROCESS_BASE = ['ffmpeg', '-y', '-i']


@utils.dec_exec_output_stream
def scale_video_args(input_: str, scale_: str, output_name_: str) -> list:
        """Scale a video to a different resolution

        Example ffmpeg command:
        ffmpeg -i ppress_1080p_16-9_23-79fps.mp4 -filter:v scale=1280:720 -c:a copy output.mp4
        
        Arguments:
            input_ {str} -- path/to/and/including/input/videoName
            scale_ {str} -- Scale string ex: '1280:70'
            output_name_ {str} -- path/to/and/including/output/videoName

        Returns:
        list -- A list of arguments required to make a subprocess call
        """
        input_file = Path(input_)
        if not input_file.is_file():
                raise Exception (f'Input: {input_}: is not a valid file.')

        args_base = FFMPEG_INPUT_PROCESS_BASE
        args = [input_, '-filter:v', f'scale={scale_}', '-c:a', 'copy', os.path.abspath(output_name_)]
        args_base.extend(args)

        return args_base

@utils.dec_exec_output_stream
def encode_and_adjust_args(input_: str, output_name_: str, bitrate_=None, fps_=None, scale_=None) -> list:
        """Encodes a video into a Matroska container, and adjusts various fields based
           on specific settings.
        
        Example ffmpeg commands:
        ffmpeg -i input.webm -c:a copy -c:v vp9 -b:v 1M output.mkv
        
        This will copy the audio from input.webm and convert the video to a VP9 codec
        with a bitrate of 1M/s, bundled up in a Matroska container.

        ffmpeg -i input.webm -c:a copy -c:v vp9 -r 30 output.mkv

        This will do the same as above, however it will force the framerate to
        30 fps.

        ffmpeg -i input.mkv -c:a copy -s 1280x720 output.mkv

        This will do the same as the first command, but will modify the video
        to 1280x720 in the output.

        Arguments:
                input_ {str} -- [description]
                output_ {str} -- [description]

        Keyword Arguments:
                bitrate_ {int} -- Bitrate of the encoded video (default: {None})
                fps_ {int} -- Desired framerate conversion (default: {None})
                scale_ {int} -- Desired scale conversion (default: {None})

        Returns:
            list -- [description]
        """
        input_file = Path(input_)
        if not input_file.is_file():
                raise Exception (f'Input: {input_}: is not a valid file.')

        args_base = FFMPEG_INPUT_PROCESS_BASE
        args = [input_, '-c:a', 'copy', '-c:v', 'vp9']
        args_base.extend(args)

        if bitrate_ and type(bitrate_) is int:
                args_base.extend(['-b:v', f'{bitrate_}M'])
        if fps_ and type(fps_) is int:
                args_base.extend(['-r', f'{fps_}'])
        if scale_ and type(scale_) is int:
                args_base.extend(['-s', f'hd{scale_}'])

        output = os.path.abspath(output_name_)
        args_base.extend([output])

        return args_base
