import os
import sys
from pathlib import Path

import ffmpeg_py.utils as utils

# FFMPEG process base executable
FFMPEG_PROCESS_BASE = ['ffmpeg']


def scale_video(input_: str, scale_: str, output_name_: str):
        """Scale a video to a different resolution

        Example ffmpeg command:
        ffmpeg -i ppress_1080p_16-9_23-79fps.mp4 -filter:v scale=1280:720 -c:a copy output.mp4
        
        Arguments:
            input_ {str} -- path/to/and/including/input/videoName
            scale_ {str} -- Scale string ex: '1280:70'
            output_name_ {str} -- path/to/and/including/output/videoName
        """
        input_file = Path(input_)
        if not input_file.is_file():
                raise Exception (f'Input: {input_}: is not a valid file.')

        args_base = FFMPEG_PROCESS_BASE
        args = ['-y', '-i', input_, '-filter:v', f'scale={scale_}', '-c:a', 'copy', output_name_]
        args_base.extend(args)

        for path in utils.execute(args_base):
                print(path, end="")
