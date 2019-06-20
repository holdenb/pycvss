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
import ffmpeg_py.ffmpeg.ffmpeg_bindings as bindings

# Sample video directory full path
SAMPLE_VIDEO_DIR = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), 'sample-video')
# Sample video 1 full path
SAMPLE_VIDEO_1 = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps.mp4')


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
    output_name = 'benchmark-scale-output.mp4'
    benchmark.pedantic(
        bindings.scale_video_args,
        args=(SAMPLE_VIDEO_1, '1280:720', output_name),
        iterations=1, rounds=1)

    assert(handle_test_cleanup(output_name))


def test_benchmark_raw_encode(benchmark):
    """Benchmark test for the scale_video function
    
    Arguments:
        benchmark {benchmark} -- pytest-benchmark object
    """
    output_name = 'benchmark-raw-encode-scale-output.mp4'
    benchmark.pedantic(
        bindings.encode_and_adjust_args,
        args=(SAMPLE_VIDEO_1, output_name),
        iterations=1, rounds=1)

    assert(handle_test_cleanup(output_name))
