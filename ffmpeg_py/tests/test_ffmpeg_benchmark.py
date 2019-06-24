import os
import sys
import pytest
import pytest_benchmark
import time
from pathlib import Path

# System path to the top level project directory
# NOTE This must be done in order for modules to be imported when running `pytest`
# at the project level
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

# Local imports
import ffmpeg_py.ffmpeg.process_args as fp_args
import ffmpeg_py.ffmpeg.calls as calls

# Sample video directory full path
SAMPLE_VIDEO_DIR = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), 'sample-video')

# Sample video full path
# NOTE We need to have multiple copies for each benchmark because FFMPEG cannot edit existing files in-place.
SAMPLE_VIDEO_1 = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps_1.mp4')
SAMPLE_VIDEO_2 = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps_2.mp4')
SAMPLE_VIDEO_3 = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps_3.mp4')


#TODO Benchmark in-place conversion vs normal conversion


def handle_test_cleanup(output_file_: str) -> bool:
    output = Path(output_file_)
    if not output.is_file:
        return False
    os.remove(output)
    return True


def test_benchmark_scale_video(benchmark):
    """Benchmark test for the scale_video function
    
    Arguments:
        benchmark {benchmark} -- pytest-benchmark object
    """
    output_name = 'benchmark-scale-video-output.mp4'
    benchmark.pedantic(
        calls.call_args_list,
        args=(fp_args.scale_video_args, SAMPLE_VIDEO_1, output_name, '1280:720'),
        iterations=1, rounds=1)

    assert(handle_test_cleanup(output_name))


def test_benchmark_raw_encode(benchmark):
    """Benchmark test for the scale_video function
    
    Arguments:
        benchmark {benchmark} -- pytest-benchmark object
    """
    output_name = 'benchmark-raw-encode-output.mkv'
    benchmark.pedantic(
        calls.call_args,
        args=(lambda: fp_args.encode_and_adjust_args(SAMPLE_VIDEO_2, output_name, 1, 30, 720)),
        iterations=1, rounds=1)

    assert(handle_test_cleanup(output_name))


def test_benchmark_modify_stream(benchmark):
    """Benchmark test for the modify stream function
    
    Arguments:
        benchmark {benchmark} -- pytest-benchmark object
    """
    output_name = 'benchmark-modify-stream-output.mp4'
    benchmark.pedantic(
        calls.call_args,
        args=(lambda: fp_args.modify_stream_args (SAMPLE_VIDEO_3, output_name, '00:00:02', 5)),
        iterations=1, rounds=1)

    assert(handle_test_cleanup(output_name))
