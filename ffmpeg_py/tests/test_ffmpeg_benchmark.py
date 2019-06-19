import os
import sys
import pytest
import pytest_benchmark

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

# Local imports
import ffmpeg.ffmpeg_bindings as ffmpeg_bindings


def test_example_benchmark (benchmark):
    benchmark (ffmpeg_bindings.resolution_conversion,
               input_=ffmpeg_bindings.SAMPLE_VIDEO_1,
               scale_='1280:720', output_name_='benchmark-output.mp4')
