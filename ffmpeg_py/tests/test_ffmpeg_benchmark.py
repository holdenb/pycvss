import os
import sys
import pytest
import pytest_benchmark
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


def test_benchmark_scale_video(benchmark):
    """Benchmark test for the scale_video function
    
    Arguments:
        benchmark {benchmark} -- pytest-benchmark object
    """
    output_name = 'benchmark-output.mp4'
    benchmark (bindings.scale_video,
               input_=SAMPLE_VIDEO_1,
               scale_='1280:720', output_name_=output_name)

    # Handle test cleanup
    output = Path(output_name)
    assert(output.is_file())
    os.remove(output_name)
    assert(not output.is_file())
