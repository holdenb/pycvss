import os
import sys
import subprocess
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

SAMPLE_VIDEO_DIR = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), 'sample-video')
SAMPLE_VIDEO_1 = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps.mp4')

FFMPEG_PROCESS_BASE = ['ffmpeg']


def execute(cmd_: list):
        """
        Executes a subprocess command
        Arguments:
        cmd {list} -- List of arguments to forward to the process

        Raises:
        subprocess.CalledProcessError:
        """
        popen = subprocess.Popen(cmd_, stdout=subprocess.PIPE, universal_newlines=True)

        for stdout_line in iter(popen.stdout.readline, ""):
                yield stdout_line 

        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
                 raise subprocess.CalledProcessError(return_code, cmd_)


def resolution_conversion(input_: str, scale_: str, output_name_: str):
        input_file = Path(input_)
        if not input_file.is_file():
                raise Exception (f'Input: {input_}: is not a valid file.')

        # Example arguments:
        # ffmpeg -i ppress_1080p_16-9_23-79fps.mp4 -filter:v scale=1280:720 -c:a copy output.mp4
        args_base = FFMPEG_PROCESS_BASE
        args = ['-y', '-i', input_, '-filter:v', f'scale={scale_}', '-c:a', 'copy', output_name_]
        args_base.extend(args)

        for path in execute(args_base):
                print(path, end="")

        # Clean up output
        os.remove(output_name_)
