import os
import sys
# import pytest
# import time
# from pathlib import Path

# System path to the top level project directory
# NOTE This must be done in order for modules to be imported when running `pytest`
# at the project level
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

# Local imports
# import ffmpeg_py.ffmpeg.process_args as fp_args
# import ffmpeg_py.ffmpeg.calls as calls


######################################################################################
# Sample video directory full path
SAMPLE_VIDEO_DIR = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), 'sample-video')

# Sample video full path
# NOTE We need to have multiple copies for each benchmark because FFMPEG cannot edit existing files in-place.
SAMPLE_VIDEO_1 = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps_1.mp4')
SAMPLE_VIDEO_2 = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps_2.mp4')
SAMPLE_VIDEO_3 = os.path.join(SAMPLE_VIDEO_DIR, 'ppress_1080p_16-9_23-79fps_3.mp4')


#TODO Add unit tests for process_args functs
