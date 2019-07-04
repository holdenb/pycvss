import os
import sys
import pycvss.ffmpeg.process_args as fp_args
import pycvss.ffmpeg.calls as calls
import pycvss.sample_files as sample_files
from pathlib import Path


######################################################################################
# Current working directory
CURRENT_DIR = os.getcwd()


def _file(output_file_: str) -> str:
    """Prepends the current path where this script is run, to an output file"""
    return os.path.join (CURRENT_DIR, output_file_)


# Output files with the current path prepended to them
OUTPUT_FILES = [
    _file('output_1.mp4'),
    _file('output_2.mp4'),
    _file('output_1.mkv'),
    _file('output_3.mp4')
]

# Benchmarking function calls
BENCHMARK_FUNCTIONS = {
    'scale_video': lambda: calls.call_log_args(lambda: fp_args.scale_video_args(
        sample_files.SAMPLE_VIDEO_1, OUTPUT_FILES[0], '1280:720')),
    'encode_and_adjust': lambda: calls.call_log_args(lambda: fp_args.encode_and_adjust_args(
        sample_files.SAMPLE_VIDEO_2, OUTPUT_FILES[1], bitrate_=1, fps_=30, scale_=720)),
    'modify_stream': lambda: calls.call_log_args(lambda: fp_args.modify_stream_args(
        sample_files.SAMPLE_VIDEO_3, OUTPUT_FILES[2], '00:00:02', 5)),
    'encode_with_gpu_cuda_accel': lambda: calls.call_log_args(lambda: fp_args.hw_accel_encode(
        sample_files.SAMPLE_VIDEO_5, OUTPUT_FILES[3], 6, 10))
}


######################################################################################
def _handle_test_cleanup(output_file_: str) -> bool:
    """ Handles the cleanup of output files"""
    try:
        output = Path(output_file_)
        os.remove(output)
    except FileNotFoundError:
        print(f"Skipping file: '{output_file_}': File not found.")


def print_sep ():
    print('-' * 100)


def _format_output (str_: str):
    print(str_)
    print_sep()


######################################################################################
if __name__ == "__main__":
    # Benchmarking outside of pytest-benchmark

    results = list()
    list(map(lambda x: results.append (x), [str('['+ name + ': ' + str(call()) + 's]') for (name, call) in BENCHMARK_FUNCTIONS.items()]))

    # Print results
    print('\n[----Benchmark results----]')
    print_sep()
    list(map(_format_output, results))
    print()

    # Clean up output files
    list(map(lambda x: _handle_test_cleanup(x), OUTPUT_FILES))
