import os
import sys
import pycvss.ffmpeg.process_args as fp_args
import pycvss.ffmpeg.calls as calls
import pycvss.sample_files as sample_files
from pathlib import Path


######################################################################################
# Keys
OUTPUT_MP4 = 'mp4'
OUTPUT_MKV = 'mkv'
OUTPUT_NAME_GRAYSCALE = 'convert_grayscale'
OUTPUT_NAME_SCALE_VID = 'scale_video'
OUTPUT_NAME_ENCODE_ADJUST = 'encode_and_adjust'
OUTPUT_NAME_MOD_STREAM = 'modify_stream'
OUTPUT_NAME_ENCODE_HW_ACCEL = "encode_with_hw_accel"

# Current working directory
CURRENT_DIR = os.getcwd()


def _file(output_file_: str) -> str:
    """Prepends the current path where this script is run, to an output file"""
    return os.path.join (CURRENT_DIR, output_file_)


# Output files with the current path prepended to them
OUTPUT_FILES = {
    OUTPUT_MP4: _file('output.mp4'),
    OUTPUT_MKV: _file('output.mkv'),
}

# Benchmarking function calls
BENCHMARK_FUNCTIONS = {
    OUTPUT_NAME_GRAYSCALE: lambda: calls.call_log_args(lambda: fp_args.grayscale_conversion_args(
        sample_files.SAMPLE_VIDEO_PPRESS, OUTPUT_FILES[OUTPUT_MP4])),
    OUTPUT_NAME_SCALE_VID: lambda: calls.call_log_args(lambda: fp_args.scale_video_args(
        sample_files.SAMPLE_VIDEO_PPRESS, OUTPUT_FILES[OUTPUT_MP4], '1280:720')),
    OUTPUT_NAME_ENCODE_ADJUST: lambda: calls.call_log_args(lambda: fp_args.encode_and_adjust_args(
        sample_files.SAMPLE_VIDEO_PPRESS, OUTPUT_FILES[OUTPUT_MKV], bitrate_=1, fps_=30, scale_=720)),
    OUTPUT_NAME_MOD_STREAM: lambda: calls.call_log_args(lambda: fp_args.modify_stream_args(
        sample_files.SAMPLE_VIDEO_DOGS, OUTPUT_FILES[OUTPUT_MP4], '00:00:02', 5)),
    OUTPUT_NAME_ENCODE_HW_ACCEL: lambda: calls.call_log_args(lambda: fp_args.hw_accel_encode(
        sample_files.SAMPLE_VIDEO_HD_MOV, OUTPUT_FILES[OUTPUT_MP4], 6, 10))
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

    #TODO A copy of the input file will have to be made before each test is run. Possibly create a benchmark or test class
    # which will handle the creation of a test with the given steps:
    # Copy the input file
    # Start benchmark
    # Process input file
    # End benchmark
    # Cleanup output file
    # Cache results
    # This needs to be done because ffmpeg cannot edit in place with the same input files

    results = list()
    list(map(lambda x: results.append (x), [str('['+ name + ': ' + str(call()) + 's]') for (name, call) in BENCHMARK_FUNCTIONS.items()]))

    # Print results
    print('\n[----Benchmark results----]')
    print_sep()
    list(map(_format_output, results))
    print()

    # Clean up output files
    list(map(lambda x: _handle_test_cleanup(x[1]), OUTPUT_FILES.items ()))
