import os
import sys
from pathlib import Path

# Needed for parent dir imports
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

# Local imports
import utils

SAMPLE_VIDEO_DIR = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), 'sample-video')
SAMPLE_VIDEO_1 = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps.mp4')

FFMPEG_PROCESS_BASE = ['ffmpeg']


def resolution_conversion(input_: str, scale_: str, output_name_: str):
        input_file = Path(input_)
        if not input_file.is_file():
                raise Exception (f'Input: {input_}: is not a valid file.')

        # Example arguments:
        # ffmpeg -i ppress_1080p_16-9_23-79fps.mp4 -filter:v scale=1280:720 -c:a copy output.mp4
        args_base = FFMPEG_PROCESS_BASE
        args = ['-y', '-i', input_, '-filter:v', f'scale={scale_}', '-c:a', 'copy', output_name_]
        args_base.extend(args)

        for path in utils.execute(args_base):
                print(path, end="")

        # Clean up output
        os.remove(output_name_)
