import os
import sys
from pathlib import Path

# System path to the top level project directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

# Local imports
import ffmpeg_py.ffmpeg.process_args as fp_args
import ffmpeg_py.ffmpeg.calls as calls
import ffmpeg_py.tests.test_ffmpeg_benchmark as tests


######################################################################################
# Current working directory
CURRENT_DIR = os.getcwd()


# TODO doc
def _file(output_file_: str) -> str:
    """Prepends the current path where this script is run, to an output file"""
    return os.path.join (CURRENT_DIR, output_file_)


# Output files with the current path prepended to them
OUTPUT_FILES = [
    _file('output_1.mp4'),
    _file('output_2.mp4'),
    _file('output_1.mkv')
]

# Benchmarking function calls
BENCHMARK_FUNCTIONS = {
    'scale_video': lambda: calls.call_log_args(lambda: fp_args.scale_video_args(
        tests.SAMPLE_VIDEO_1, OUTPUT_FILES[0], '1280:720')),
    'encode_and_adjust': lambda: calls.call_log_args(lambda: fp_args.encode_and_adjust_args(
        tests.SAMPLE_VIDEO_2, OUTPUT_FILES[1], bitrate_=1, fps_=30, scale_=720)),
    'modify_stream': lambda: calls.call_log_args(lambda: fp_args.modify_stream_args(
        tests.SAMPLE_VIDEO_3, OUTPUT_FILES[2], '00:00:02', 5))
}


# TODO doc
def _handle_test_cleanup(output_file_: str) -> bool:
    """ Handles the cleanup of output files"""
    try:
        output = Path(output_file_)
        os.remove(output)
    except FileNotFoundError:
        print(f"Skipping file: '{output_file_}': File not found.")


# TODO command line args to optionally cleanup output files
if __name__ == "__main__":
    # Benchmarking outside of pytest-benchmark

    # TODO inject a formatting function into the list comprehension when extracting calls from the benchmarking map
    list(map(lambda x: print(x + '\n'), [str(name + ': ' + str(call())) for (name, call) in BENCHMARK_FUNCTIONS.items()]))

    # Clean up output files
    list(map(lambda x: _handle_test_cleanup(x), OUTPUT_FILES))
