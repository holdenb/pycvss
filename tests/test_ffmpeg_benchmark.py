import os
import sys
import pytest
import pytest_benchmark

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Local imports
from benchmarking import ffmpeg_benchmark


def test_example_benchmark (benchmark):
    benchmark (ffmpeg_benchmark.example_benchmark)
    assert (True)
