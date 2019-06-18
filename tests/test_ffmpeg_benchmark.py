import os
import sys
import pytest
import pytest_benchmark

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Local imports
from benchmarking import ffmpeg_benchmark


def test_example_benchmark (benchmark):
    benchmark (ffmpeg_benchmark.resolution_conversion,
               input_=ffmpeg_benchmark.SAMPLE_VIDEO_1,
               scale_='1280:720', output_name_='benchmark-output.mp4')
