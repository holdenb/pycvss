import os
import sys

# System path to the top level project directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

# Local imports
import apps.motion_capture.detection as detection
import ffmpeg_py.tests.test_ffmpeg_benchmark as tests


if __name__ == "__main__":
    # Testing the detector
    detector = detection.Detector()
    detector.input_file = tests.SAMPLE_VIDEO_5
    detector.process()
